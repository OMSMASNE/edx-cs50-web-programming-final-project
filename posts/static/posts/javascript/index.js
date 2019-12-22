/*
    Copyright (C) 2019 OM SANTOSHKUMAR MASNE. All Rights Reserved.
    Licensed under the GNU Affero General Public License v3.0 only (AGPL-3.0-only) license.
    See License.txt in the project root for license information.
*/

var posts_route = 'post';

document.addEventListener('DOMContentLoaded', startup);


// This function sends an AJAX request to the server to get the list of most recently uploaded posts.
// Then the recieved data is processed and displayed in the recent posts section.
function startup()
{
    request = new XMLHttpRequest();
    request.open('GET', '/api/get-recent-posts/');
    request.send();
    request.onload = () => {
        const data = request.responseText;
        if(data)
        {
            data_recieved = JSON.parse(data);

            // If no posts are recieved display a note.
            if(data_recieved.posts_list.length == 0)
            {
                const note_span = document.createElement('span');
                note_span.innerText = "No recent posts to display!";
                note_span.setAttribute('class', 'no-posts-note');
                document.getElementById('recent-posts').append(note_span);
            }

            posts = data_recieved.posts_list
            for(i=0; i<posts.length; i++)
            {
                const section_separator = document.createElement('hr');
                const post_box_link = document.createElement('a');
                const post_box = document.createElement('div');
                const post_box_title = document.createElement('div');
                const post_box_author_name = document.createElement('div');
                const post_box_date = document.createElement('div');
                post_box.setAttribute('class', 'post-box');
                post_box_title.setAttribute('class', 'post-box-title');
                post_box_author_name.setAttribute('class', 'post-box-author-name');
                post_box_date.setAttribute('class', 'post-box-date');
                post_box_title.innerText = posts[i].post_title;
                post_box_author_name.innerText = 'Author : ' + posts[i].author_name;
                post_box_date.innerText = 'Date and Time : ' + posts[i].date;

                post_box.append(post_box_title, section_separator, post_box_author_name, post_box_date);
                var post_link = '/' + posts_route + '/' + posts[i].author_name + '/' + posts[i].post_title;
                post_box_link.setAttribute('href', post_link);
                post_box_link.setAttribute('class', 'post-box-link');
                post_box_link.append(post_box);

                document.getElementById('recent-posts').append(post_box_link);
            }
        }
    }
}
