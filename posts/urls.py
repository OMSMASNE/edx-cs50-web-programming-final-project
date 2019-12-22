# Copyright (C) 2019 OM SANTOSHKUMAR MASNE. All Rights Reserved.
# Licensed under the GNU Affero General Public License v3.0 only (AGPL-3.0-only) license.
# See License.txt in the project root for license information.

from django.urls import path

from . import views

app_name = 'posts'

post_direct_url = 'post-direct/'

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('account-login', views.account_login, name='account-login'),
    path('signup/', views.signup, name='signup'),
    path('create-account/', views.create_account, name='create-account'),
    path('profile/', views.profile, name='profile'),
    path('post-editor/', views.post_editor, name='post-editor'),
    path('post-preview/', views.post_preview, name='post-preview'),
    path('post-preview-display/', views.post_preview_display, name='post-preview-display'),
    path('new-post/', views.new_post, name='new-post'),
    path('author/<str:author_name>/', views.author, name='author'),
    path('post/<str:author_name>/<str:post_title>/', views.post, name='post'),
    path((post_direct_url + '<str:post_id>/'), views.post_direct, name='post-direct'),
    path('api/check-username/', views.api_check_username, name='api-check-username'),
    path('api/get-post-body/', views.api_get_post_body, name='api-get-post-body'),
    path('api/save-post/', views.api_save_post, name='api-save-post'),
    path('api/get-recent-posts/', views.api_get_recent_posts, name='api-get-recent-posts'),
    path('api/check-post-title/', views.api_check_post_title, name='api-check-post-title'),
]
