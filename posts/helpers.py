# Copyright (C) 2019 OM SANTOSHKUMAR MASNE. All Rights Reserved.
# Licensed under the GNU Affero General Public License v3.0 only (AGPL-3.0-only) license.
# See License.txt in the project root for license information.

from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from .models import Posts, Custom_User

import markdown
import time
import os


# This function processes the user's post files and generates the preview files.
# It returns the post_id and optionally preview file's url.
def preview(recieved_file, user_id, return_url = True):
    user_id = str(user_id)
    media_temp_location = settings.MEDIA_TEMP
    current_time = str(round(time.time()))
    preview_filename = str(user_id + '-' + current_time + '.md')
    preview_output_filename = str(user_id + '-' + current_time + '.html')

    # Saves the recieved file.
    fs = FileSystemStorage(location=media_temp_location)
    fs.save(preview_filename, recieved_file)

    # Absolute paths for the input and output files.
    input_file = os.path.join(media_temp_location, preview_filename)
    output_file = os.path.join(media_temp_location, preview_output_filename)

    # Converts the markdown file to HTML output file.
    markdown.markdownFromFile(input = input_file, output = output_file, encoding = 'utf-8')

    # Creates the post_id.
    post_id = str(user_id + '-' + current_time)

    if return_url is True:
        new_url = settings.MEDIA_TEMP_URL + preview_output_filename
        return new_url, post_id
    else:
        return post_id


# This function is used to save the submitted post file to database.
# Also performs the waste files cleanup.
def create_post(post_id, user_id, title):
    post_status = False
    try:
        author = User.objects.get(id = user_id)
        author_name = author.username
        file_name = str(post_id) + '.html'

        media_temp_location = settings.MEDIA_TEMP
        file_location = os.path.join(media_temp_location, file_name)

        with open(file_location, 'r') as f:
            file_id = File(f)
            post = Posts()
            post.post_id = post_id
            post.title = title
            post.author_name = author_name
            post.author_id = user_id
            post.file_id.save(file_name, file_id, save = False)
            post.save()

            # Adding the new post id to the list of author's posts_ids.
            # If posts_ids is empty, set the posts_ids as post_id.
            try:
                cu = Custom_User.objects.get(custom_username = author_name)
                if cu.posts_ids is None:
                    cu.posts_ids = str(post_id)
                else:
                    cu.posts_ids = str(cu.posts_ids) + ',' + str(post_id)
                cu.save()
            except Custom_User.DoesNotExist:
                post_status = False
                return post_status
            finally:
                temp_files_cleaner(post_id)

        post_status = True
    except:
        post_status = False

    return post_status


# This function is used to save the edited files.
def save_edited_post(new_post_file_name, old_post_id, new_post_title):
    post_status = False
    try:
        post = Posts.objects.get(id = old_post_id)

        new_post_file_name = str(new_post_file_name) + '.html'

        media_temp_location = settings.MEDIA_TEMP
        file_location = os.path.join(media_temp_location, new_post_file_name)

        with open(file_location, 'r') as f:
            file_id = File(f)
            post.file_id.save(new_post_file_name, file_id, save = False)
            post.title = new_post_title
            post.save()

        try:
            # Removes the '.html' from the end of the string
            file_name = new_post_file_name[:-5]
            temp_files_cleaner(file_name)
        except:
            pass

        post_status = True
    except:
        post_status = False

    return post_status


# This function is used to clean up the post preview files.
def temp_files_cleaner(post_id):
    media_temp_location = settings.MEDIA_TEMP
    try:
        file_name = str(post_id)
        file_location_of_html = os.path.join(media_temp_location, file_name + '.html')
        file_location_of_md = os.path.join(media_temp_location, file_name + '.md')
        os.remove(file_location_of_html)
        os.remove(file_location_of_md)
    except:
        pass
    return 0


# This function is used to return the recent posts' information.
# The information of only certain posts is send (as per the SEARCH_LIMIT).
def get_recent_posts(user):
    # Gets author object.
    # If the given username does not exists, return an empty list for recent_posts and False for old_posts.
    try:
        author = Custom_User.objects.get(custom_username = user.username)
    except Custom_User.DoesNotExist:
        return [], False

    old_posts = False
    check_old_posts = False
    SEARCH_LIMIT = 5
    try:
        user_posts = author.posts_ids
        user_posts = (user_posts.split(","))[:SEARCH_LIMIT]
        check_old_posts = True
    except:
        check_old_posts = False

    recent_posts_titles = []
    recent_posts_links = []

    if check_old_posts is True:
        if len(user_posts) == 0:
            old_posts = False
        else:
            for i in range(0, len(user_posts)):
                if user_posts[i] == None:
                    continue
                post = Posts.objects.get(post_id = user_posts[i])
                recent_posts_titles.append(post.title)
                post_link = '/post' + '/' + author.custom_username + '/' + post.title
                recent_posts_links.append(post_link)
            old_posts = True

    recent_posts = zip(recent_posts_titles, recent_posts_links)
    return recent_posts, old_posts


# This function is used to return all previous posts' information.
def get_all_previous_posts(user):
    # Gets author object.
    # If the given username does not exists, return an empty list for recent_posts and False for old_posts.
    try:
        author = Custom_User.objects.get(custom_username = user.username)
    except Custom_User.DoesNotExist:
        return [], False

    old_posts = False
    check_old_posts = False
    try:
        user_posts = author.posts_ids
        user_posts = user_posts.split(",")
        check_old_posts = True
    except:
        check_old_posts = False

    recent_posts_titles = []
    recent_posts_ids = []

    if check_old_posts is True:
        if len(user_posts) == 0:
            old_posts = False
        else:
            for i in range(0, len(user_posts)):
                post = Posts.objects.get(post_id = user_posts[i])
                recent_posts_titles.append(post.title)
                post_id = post.post_id
                recent_posts_ids.append(post_id)
            old_posts = True

    recent_posts = zip(recent_posts_titles, recent_posts_ids)
    return recent_posts, old_posts
