# Copyright (C) 2019 OM SANTOSHKUMAR MASNE. All Rights Reserved.
# Licensed under the GNU Affero General Public License v3.0 only (AGPL-3.0-only) license.
# See License.txt in the project root for license information.

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from .models import Posts, Custom_User

import json
from . import helpers
from . import urls


# This function acts as the homepage or '/' route of the website.
def index(request):
    user = request.user
    context = {'user_logged_in':False}

    if request.user.is_authenticated:
        username = user.get_username()
        context = {'username':username, 'user_logged_in':True}

    return render(request, "posts/index.html", context)


# This function is used to display the login page.
def login_page(request):
    return render(request, "posts/login.html")


# This function logs out the user and displays the logout page.
def logout_page(request):
    logout(request)
    context = {'from':"ACCOUNT LOGOUT:", 'message':"LOGGED OUT SUCCESSFULLY!"}
    return render(request, "posts/misc.html", context)


# This function is user to authenticate the user and login the user.
# If authentication is successful, then, the user is redirected to the homepage.
# If the authentication is not successful, then, an invalid credentials page is displayed.
def account_login(request):
    username = request.POST.get('username')
    password = str(request.POST.get('password'))

    user = authenticate(request, username = username, password = password)

    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("posts:home"))
    else:
        context = {'from':"ACCOUNT LOGIN ERROR:", 'message':"INVALID CREDENTIALS!"}
        return render(request, "posts/misc.html", context)


# This function is used to display the signup page.
def signup(request):
    return render(request, "posts/signup.html")


# This function is used to create a new account.
def create_account(request):
    username = str(request.POST.get('username'))
    password = str(request.POST.get('password'))
    email = str(request.POST.get('email'))
    first_name = str(request.POST.get('first_name'))
    last_name = str(request.POST.get('last_name'))
    info = ['Username : ' + username, 'Password : ' + password, 'Email : ' + email, 
    'First Name : ' + first_name, 'Last Name : ' + last_name]

    # Checks for invalid username or password or email field.
    if (username or password or email) == "":
        context = {'from':'NEW ACCOUNT NOT CREATED!', 'message':'Invalid username or password or email', 'info':info}
        return render(request, "posts/misc.html", context)

    # Checks if the username is already taken or not.
    if (username or password) is not None:
        try:
            check_user_exist = User.objects.get(username = username)
            check_user_exist = True
        except User.DoesNotExist:
            check_user_exist = False

        # If the username is not available, then, an error page is shown.
        if check_user_exist is True:
            context = {'from':'NEW ACCOUNT NOT CREATED!', 'message':'Username already taken!', 'info':info}
            return render(request, "posts/misc.html", context)

        # Creates the user with the provided data.
        user = User.objects.create_user(username = username, password = password, email = email,
        first_name = first_name, last_name = last_name)
        user.save()

        # Create the Custom_User for storing the user's posts_ids.
        cu = Custom_User(user = user, custom_username = user.username)
        cu.save()

    context = {'from':'NEW ACCOUNT CREATED!', 'message':'NEW ACCOUNT CREATED!', 'info':info}
    context['new_account_status'] = 'true'
    return render(request, "posts/misc.html", context)


# This function is used to display the user's profile.
def profile(request):
    user = request.user
    user_logged_in = False

    if not user.is_authenticated:
        return HttpResponseRedirect(reverse("posts:home"))

    username = str(user.get_username())
    user_logged_in = True
    full_name = str(user.first_name + ' ' + user.last_name)

    # Used to obtain the recent posts' titles and post links.
    recent_posts, old_posts = helpers.get_recent_posts(user)

    context = {'user_logged_in': user_logged_in, 'username':username, 'author_username':username, 'full_name':full_name, 'email':user.email}
    context['recent_posts'] = recent_posts
    context['message'] = 'false'
    context['recent_posts_status'] = old_posts

    # If a message is supplied with the url (via GET request), then, it is shown on the webpage.
    message = request.GET.get('message')
    if message is not None:
        context['message'] = message

    return render(request, "posts/profile.html", context)


# This function is used to display an author's information.
def author(request, author_name):
    user = request.user
    user_logged_in = False
    if not user.is_authenticated:
        user_logged_in = False
        username = ''
    else:
        user_logged_in = True
        username = str(user.get_username())

    try:
        author = User.objects.get(username = author_name)
    except:
        context = {'from':'Posts', 'message':'Author not found!'}
        return render(request, 'posts/misc.html', context)

    # Used to obtain the recent posts' titles and post links.
    recent_posts, old_posts = helpers.get_recent_posts(author)

    full_name = str(author.first_name + ' ' + author.last_name)
    context = {'user_logged_in': user_logged_in, 'username':username, 'author_username':author.username, 'full_name':full_name, 'email':author.email, 'recent_posts':recent_posts}
    context['message'] = 'false'
    context['recent_posts_status'] = old_posts

    return render(request, "posts/profile.html", context)


# This function is used to display the requested post.
# It takes the author's name and post's title to obtain the proper post.
def post(request, author_name, post_title):
    user = request.user
    user_logged_in = False
    if not user.is_authenticated:
        user_logged_in = False
        username = ''
    else:
        user_logged_in = True
        username = str(user.get_username())

    # Checks if the author's name exists, else, displays an error message.
    try:
        author = User.objects.get(username = author_name)
    except:
        context = {'from':'Posts', 'message':'Author not found!'}
        return render(request, 'posts/misc.html', context)

    # Checks if the requested post exists, else, displays an error message.
    try:
        post = Posts.objects.get(title = post_title, author_name = author_name)
    except:
        context = {'from':'Posts', 'message':'Post not found!'}
        return render(request, 'posts/misc.html', context)

    post_date = post.creation_date

    text = post.file_id.read()
    text = text.decode('utf-8')

    post_link = '/' + urls.post_direct_url + post.post_id

    context = {'username':username, 'post_text':text}
    context['post_title'] = post_title
    context['author_name'] = author_name
    context['post_date'] = post_date
    context['user_logged_in'] = user_logged_in
    context['post_link'] = post_link
    return render(request, 'posts/post.html', context)


# This function is used to display the post, directly by using the post_id.
def post_direct(request, post_id):
    user = request.user
    user_logged_in = False
    if not user.is_authenticated:
        user_logged_in = False
        username = ''
    else:
        user_logged_in = True
        username = str(user.get_username())

    try:
        post = Posts.objects.get(post_id = post_id)
    except:
        context = {'from':'Posts', 'message':'Post not found!'}
        return render(request, 'posts/misc.html', context)

    text = post.file_id.read()
    text = text.decode('utf-8')

    post_link = '/' + urls.post_direct_url + post.post_id

    context = {'username':username, 'post_text':text}
    context['post_title'] = post.title
    context['author_name'] = post.author_name
    context['post_date'] = post.creation_date
    context['user_logged_in'] = user_logged_in
    context['post_link'] = post_link
    return render(request, 'posts/post.html', context)


# This function is used to display the post editor (post manager) page.
def post_editor(request):
    user = request.user
    user_logged_in = False

    if not user.is_authenticated:
        return HttpResponseRedirect(reverse("posts:home"))

    username = str(user.get_username())

    user_logged_in = True
    context = {'user_logged_in':user_logged_in, 'username':username}

    # Used to obtain the titles and post_id(s) of the user's all submitted posts.
    previous_posts, old_posts = helpers.get_all_previous_posts(user)

    context['old_posts'] = old_posts
    context['previous_posts'] = previous_posts

    return render(request, 'posts/post_editor.html', context)


# This function is used to process the new posts created by the users.
# It generates the post preview link, post_id.
@csrf_exempt
def post_preview(request):
    user = request.user

    if not user.is_authenticated:
        return HttpResponseRedirect(reverse("posts:home"))

    try:
        send_type = str(request.POST.get('send-type'))

        print('\n\n\n\nTESTINGS')
        print('send_type = ' + send_type)
        print('FILES : ' + str(request.FILES))

        post_title = request.POST.get('post-title')

        # Checks if the title is available or not.
        check_post_exist = False
        try:
            author_name = str(user.get_username())
            post = Posts.objects.get(title = post_title, author_name = author_name)
            check_post_exist = True
        except Posts.DoesNotExist:
            check_post_exist = False

        if check_post_exist is True:
            context = {'from':'Post Preview', 'message':'Chosen post title is already used by you!'}
            return render(request, 'posts/misc.html', context)

        # Handles the user's uploaded file.
        recieved_file = request.FILES['post-file']

        recieved_file_name = str(recieved_file.name)
        required_type = ('.txt', '.md')
        if not recieved_file_name.endswith(required_type):
            context = {'from':'Post Preview', 'message':'File type is not correct!'}
            return render(request, 'posts/misc.html', context)

        # Used to generate the preview files for the user's new post.
        user_id = user.id
        new_url, post_id = helpers.preview(recieved_file, user_id, return_url=True)

        url = reverse("posts:post-preview-display")
        url = url + '?' + 'post_preview_link=' + new_url + '&' + 'post_id=' + post_id + '&' + 'post_title=' + post_title
        return HttpResponseRedirect(url)

    except:
        context = {'from':'Post Preview', 'message':'Something went wrong!'}
        return render(request, 'posts/misc.html', context)


# This function is used to display the newly created posts preview.
# It also provides the option to submit the post or discard it.
def post_preview_display(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect(reverse("posts:home"))
    else:
        user_logged_in = True
        username = str(user.get_username())

    try:
        post_id = request.GET.get('post_id')
        post_title = request.GET.get('post_title')
        new_url = request.GET.get('post_preview_link')
        context = {'user_logged_in':user_logged_in, 'username':username, 'post_preview_link':new_url,
            'post_id':post_id, 'post_title':post_title}
        return render(request, 'posts/post_preview.html', context)

    except:
        context = {'from':'Post Preview', 'message':'Something went wrong!'}
        return render(request, 'posts/misc.html', context)


# This function is used to submit the new posts, or, discard the previewed post.
def new_post(request):
    user = request.user

    if not user.is_authenticated:
        return HttpResponseRedirect(reverse("posts:home"))

    new_post = request.POST.get('new-post')
    post_id = request.POST.get('post-id')
    post_title = request.POST.get('post-title')
    if new_post == 'true':
        # Used to submit the new post of the user.
        post_status = helpers.create_post(post_id, user.id, post_title)
        if post_status:
            message = 'Your post: ' + post_title + ' was Submitted!'
        else:
            message = 'Post not Submitted! Please try again!'
    else:
        # Used to clean up the preview files.
        helpers.temp_files_cleaner(post_id)
        message = 'Your post was not submitted!'

    url = reverse("posts:profile") + '?' + 'message=' + message
    return HttpResponseRedirect(url)


# This function checks if an username already exists.
# It sends its response to the signup page for checking the user's entered username's availability.
@csrf_exempt
def api_check_username(request):
    username = str(request.POST.get('username'))
    availability = False
    check_user_exist = False

    try:
        check_user_exist = User.objects.get(username = username)
        check_user_exist = True
    except User.DoesNotExist:
        check_user_exist = False

    if check_user_exist is True:
        availability = False
    else:
        availability = True

    context = {'username_availability': availability}
    return HttpResponse(json.dumps(context))


# This function is used to send the requested post's body (content).
@csrf_exempt
def api_get_post_body(request):
    post_found = False
    post_body = ''
    author_name = str(request.POST.get('post_author'))
    post_title = str(request.POST.get('post_title'))
    try:
        post = Posts.objects.get(title = post_title, author_name = author_name)
        text = post.file_id.read()
        text = text.decode('utf-8')
        post_body = text
        post_found = True
    except:
        post_found = False

    context = {'post_found':post_found, 'post_body':post_body}
    return HttpResponse(json.dumps(context))


# This function is used to save the changes of an existing post.
@csrf_exempt
def api_save_post(request):
    user = request.user
    user_id = user.id
    post_found = False
    post_saved = False
    author_name = str(request.POST.get('post_author'))
    old_post_title = str(request.POST.get('old_post_title'))
    new_post_title = str(request.POST.get('new_post_title'))
    recieved_file = request.FILES['post_file']

    try:
        post = Posts.objects.get(title = old_post_title, author_name = author_name)
        post_found = True
        old_post_id = post.id

        try:
            # Used to process the user's edited post.
            new_post_file_id = helpers.preview(recieved_file, user_id, return_url=False)

            # Used to save the user's edited post.
            post_saved = helpers.save_edited_post(new_post_file_id, old_post_id, new_post_title)
        except:
            post_saved = False

    except:
        post_found = False

    context = {'post_found':post_found, 'post_saved':post_saved}

    return HttpResponse(json.dumps(context))


# This function is used to send the recently published posts' information.
# It send at most the 5 new posts' information.
def api_get_recent_posts(request):
    posts = Posts.objects.order_by('-pk')

    if len(posts) > 5:
        posts = posts[:5]

    posts_list = []
    for post in posts:
        date = post.creation_date.strftime("%x %X")
        post = {'post_title':post.title, 'author_name':post.author_name, 'date':date}
        posts_list.append(post)

    context = {'posts_list':posts_list}
    return HttpResponse(json.dumps(context))


# This function is used to check if the user's selected title has already been used by the same user.
# This helps to prevent same titles collisions.
@csrf_exempt
def api_check_post_title(request):
    author_name = str(request.POST.get('username'))
    post_title = str(request.POST.get('post_title'))
    availability = False
    check_post_exist = False

    try:
        post = Posts.objects.get(title = post_title, author_name = author_name)
        check_post_exist = True
    except Posts.DoesNotExist:
        check_post_exist = False

    if check_post_exist is True:
        availability = False
    else:
        availability = True

    context = {'post_title_availability': availability}
    return HttpResponse(json.dumps(context))
