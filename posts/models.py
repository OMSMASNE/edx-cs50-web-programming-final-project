# Copyright (C) 2019 OM SANTOSHKUMAR MASNE. All Rights Reserved.
# Licensed under the GNU Affero General Public License v3.0 only (AGPL-3.0-only) license.
# See License.txt in the project root for license information.

from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class Posts(models.Model):
    post_id = models.CharField(max_length = 40, null = True)
    title = models.CharField(max_length = 100)
    author_name = models.CharField(max_length = 40)
    author_id = models.CharField(max_length = 40)
    creation_date = models.DateTimeField(auto_now_add=True)
    file_id = models.FileField(upload_to='posts/', max_length=200)

    def __str__(self):
        return self.title


class Custom_User(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    custom_username = models.CharField(max_length=100, null=True, blank=True)
    posts_ids = models.CharField(max_length = 2000, null=True, blank=True)
