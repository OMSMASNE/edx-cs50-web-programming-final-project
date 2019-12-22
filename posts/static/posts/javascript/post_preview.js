/*
    Copyright (C) 2019 OM SANTOSHKUMAR MASNE. All Rights Reserved.
    Licensed under the GNU Affero General Public License v3.0 only (AGPL-3.0-only) license.
    See License.txt in the project root for license information.
*/

var post_id = '';
var post_title = '';

document.addEventListener('DOMContentLoaded', startup);

// Sets up the necessary conditions, when the page is loaded.
function startup()
{
    document.getElementById('approve-post').addEventListener('click', approve_post);
    document.getElementById('change-post').addEventListener('click', cancel_post);
    post_id = document.getElementById('post-id').value;
    post_title = document.getElementById('post-title-value').value;
}

// Listens for clicks on the approve post button.
function approve_post()
{
    submit_post('true');
}

// Listens for clicks on the cancel post submission button.
function cancel_post()
{
    submit_post('false')
}

// This function processes the user's decision about the post.
// It also informs the decision to the server via a form submission.
function submit_post(approved)
{
    const myForm = document.getElementById('decision-form');
    myForm.action = "/new-post/";
    myForm.method = 'POST';

    if(approved == 'true')
    {
        var params = {'new-post':'true', 'post-id':post_id, 'post-title':post_title};
    }
    else
    {
        var params = {'new-post':'false', 'post-id':post_id, 'post-title':post_title};
    }

    for(const key in params)
    {
        if(params.hasOwnProperty(key))
        {
            const hidden_element = document.createElement('input');
            hidden_element.type = 'hidden';
            hidden_element.name = key;
            hidden_element.value = params[key];
            myForm.appendChild(hidden_element);
        }
    }

    document.body.appendChild(myForm);
    myForm.submit();
}
