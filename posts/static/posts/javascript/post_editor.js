/*
    Copyright (C) 2019 OM SANTOSHKUMAR MASNE. All Rights Reserved.
    Licensed under the GNU Affero General Public License v3.0 only (AGPL-3.0-only) license.
    See License.txt in the project root for license information.
*/

var post_title = '';
var post_body = '';
var send_type = '';
var file_to_upload = '';
var author = '';
var old_post_title = '';
var new_post_title = '';
var placeholder_text = 'Write the post here!\nSelect the text to format and edit it!';

var editor;
var file_from_text;

document.addEventListener("DOMContentLoaded", startup);

// Sets the necessary styling when the page is loaded.
function startup()
{
    document.getElementById('create-new-post-btn').addEventListener('click', new_post);
    document.getElementById('post-edit-btn').addEventListener('click', edit_old_post);
    document.getElementById('upload-post').addEventListener('click', post_upload);
    document.getElementById('submit-new-post-btn').addEventListener('click', submit_post);
    document.getElementById('write-post-here').addEventListener('click', type_new_post);
    document.getElementById('save-post-btn').addEventListener('click', save_edited_post);
    document.getElementById('new-post-surface').style.display = 'none';
    document.getElementById('post-editor-container').style.display = 'none';
    document.getElementById('new-post-creator').style.display = 'none';
    document.getElementById('file-to-upload-name-container').style.display = 'none';

    document.getElementById('new-post-title-input').value = '';
    document.getElementById('new-post-textarea').value = '';
    document.getElementById('file-upload-input').value = '';
    document.getElementById('new-post-title-input').addEventListener('blur', check_post_title);
    document.getElementById('edit-post-title-input').addEventListener('blur', check_post_title);

    document.getElementById('file-upload-input').addEventListener('change', display_file_name);
}

// It checks if the current post title is available or not.
function check_post_title()
{
    console.log('Checking title!');
    var status = false;
    let post_title_element = document.getElementById('new-post-title-input');
    let author_name = document.getElementById('username').value;
    let new_post_title = document.getElementById('edit-post-title-input').value;

    const request = new XMLHttpRequest();
    const data = new FormData();
    data.append('username', author_name);
    if(new_post_title == "")
    {
        console.log('PT : ' + post_title_element.value);
        data.append('post_title', post_title_element.value);
    }
    else
    {
        console.log('PT : ' + new_post_title);
        data.append('post_title', new_post_title);
    }

    request.open('POST', '/api/check-post-title/');
    request.send(data);
    request.onload = () => {
        const data = request.responseText;
        if(data)
        {
            data_recieved = JSON.parse(request.responseText);
            console.log(data_recieved.post_title_availability);
            if(!data_recieved.post_title_availability)
            {
                if(old_post_title == "")
                {
                    alert('Post title is not available!\n\nPlease choose different Post Title.');
                    post_title_element.value = '';
                    status = false;
                }
                else
                {
                    if(new_post_title != old_post_title)
                    {
                        alert('Post title is not available!\n\nPlease choose different Post Title.');
                    }
                }
            }
            else
            {
                status = true;
            }
            request_complete = true;
        }
    }
    return status;
}

// Sets the necessary styling, when the user clicks new post button.
function new_post()
{
    console.log('New post!');
    hide_option_selector();
    document.getElementById('new-post-surface').style.display = 'block';
    document.getElementById('new-post-surface').style.animation = 'introduce-card 2s forwards 1';
    document.getElementById('new-post-surface').addEventListener('animationend', () => {
        document.getElementById('new-post-surface').style.animation = '';
    });
}

// Sets the necessary styling, when the user wants to write a new post.
// It also initialises the MediumEditor for editing the text.
function type_new_post()
{
    console.log('Write new post!');
    document.getElementById('new-post-creator').style.display = 'block';
    document.getElementById('new-post-creator').style.animation = 'fade-in 2s forwards 1';
    document.getElementById('new-post-creator').addEventListener('animationend', () => {
        document.getElementById('new-post-creator').style.animation = '';
    });

    document.getElementById('upload-post').setAttribute('disabled', true);
    document.getElementById('upload-post').setAttribute('class', 'btn-style-2-disabled');

    send_type = 'typed-post';

    // Initilise the MediumEditor.
    editor = new MediumEditor('.editable',{
        placeholder: {
            text: placeholder_text,
            hideOnClick: false
        }
    });
}

// Sets the necessary stlying, when the user wants to edit an old post.
// It fetches the old post via AJAX request and initialises the MediumEditor for editing the text.
function edit_old_post()
{
    console.log('Edit old post!');
    hide_option_selector();
    document.getElementById('post-editor-container').style.display = 'block';
    document.getElementById('post-editor-container').style.animation = 'introduce-card 2s forwards 1';
    document.getElementById('post-editor-container').addEventListener('animationend', () => {
        document.getElementById('post-editor-container').style.animation = '';
    });

    var select_element = document.getElementById('old-posts-selection');
    var text = select_element.value;
    document.getElementById('edit-post-title-input').value = text;

    author = document.getElementById('username').value;
    post_title = text;
    console.log('Author : ' + author);
    console.log('Post title : ' + post_title);

    const request = new XMLHttpRequest();
    const data = new FormData();
    data.append('post_author', author);
    data.append('post_title', post_title);
    request.open('POST', '/api/get-post-body/');
    request.send(data);
    request.onload = () => {
        const data = request.responseText;
        if(data)
        {
            data_recieved = JSON.parse(request.responseText);
            if(data_recieved.post_found)
            {
                console.log('POST FOUND!');
                document.getElementById('edit-post-textarea').innerHTML = data_recieved.post_body;
                old_post_title = post_title;

                // Initilise the MediumEditor.
                editor = new MediumEditor('.editable',{
                    placeholder: {
                        text: placeholder_text,
                        hideOnClick: false
                    }
                });
            }
            else
            {
                setTimeout(() => {
                    console.log('Post not found!');
                    alert('Post not Found!\n\nReloading page!');
                    location.reload();
                }, 2000);
            }
        }
    }
}

// This function is used to submit the new post to the server.
// It is used to upload both file-upload posts and user written posts.
function submit_post()
{
    console.log('Submitting post!');
    const post_title = document.getElementById('new-post-title-input').value;


    const myForm = document.createElement('form');
    myForm.action = "/post-preview/";
    myForm.method = 'POST';
 
    if(send_type == 'file-upload')
    {
        send_type = 'file-upload';
        file_to_upload = document.getElementById('file-upload-input').files;
    }
    else
    {
        send_type = 'typed-post';

        post_body = document.getElementById('new-post-textarea').innerHTML;

        // Converting the string(innerHTML) to an array.
        post_body = [post_body];

        file_from_text = new File(post_body, 'file_from_text.md');

        dt = new DataTransfer();
        dt.items.add(file_from_text);
        document.getElementById('file-upload-input').files = dt.files;
        file_to_upload = document.getElementById('file-upload-input').files;
    }

    var params = {'send-type':send_type, 'post-title':post_title, 'post-file':file_to_upload};

    for(const key in params)
    {
        if(key == 'post-file')
        {
            const hidden_element = document.createElement('input');
            hidden_element.type = 'file';
            hidden_element.name = 'post-file';
            hidden_element.files = params[key];
            hidden_element.setAttribute('hidden', '');
            myForm.appendChild(hidden_element);
            continue;
        }
        if(params.hasOwnProperty(key))
        {
            const hidden_element = document.createElement('input');
            hidden_element.type = 'hidden';
            hidden_element.name = key;
            hidden_element.value = params[key];
            myForm.appendChild(hidden_element);
        }
    }

    myForm.setAttribute('enctype', "multipart/form-data")
    document.body.appendChild(myForm);
    myForm.submit();
}

// This function is used to handle the file-upload of posts.
function post_upload()
{
    console.log('Uploading post!');
    send_type = 'file-upload';

    post_title = document.getElementById('new-post-title-input').value;
    if(post_title == '')
    {
        alert('Choose a title first!');
        return false;
    }

    alert('Please upload a Plain text or a MARKDOWN document!');

    const file_to_upload = document.getElementById('file-upload-input');
    file_to_upload.click();

    document.getElementById('write-post-here').setAttribute('disabled', true);
    document.getElementById('write-post-here').setAttribute('class', 'btn-style-2-disabled');
}

// This function is used to upload the edited old post to the server.
function save_edited_post()
{
    console.log('Submitting post!');

    new_post_title = document.getElementById('edit-post-title-input').value;

    post_body = document.getElementById('edit-post-textarea').innerHTML;

    // Converting the string(innerHTML) to an array.
    post_body = [post_body];

    var file_to_upload = new Blob(post_body, {type:'text/html'});

    const request = new XMLHttpRequest();
    const data = new FormData();
    data.append('post_author', author);
    data.append('old_post_title', old_post_title);
    data.append('new_post_title', new_post_title);
    data.append('post_file', file_to_upload);
    request.open('POST', '/api/save-post/');
    request.send(data);
    request.onload = () => {
        const data = request.responseText;
        if(data)
        {
            data_recieved = JSON.parse(request.responseText);
            if(data_recieved.post_found)
            {
                console.log('POST FOUND!');

                if(data_recieved.post_saved)
                {
                    alert('Post saved succesfully!');
                    console.log('POST SAVED!');

                    if(old_post_title != new_post_title)
                    {
                        location.reload();
                    }
                }
                else
                {
                    alert('The post was not saved!');
                    console.log('POST NOT SAVED!');
                }
            }
            else
            {
                setTimeout(() => {
                    console.log('Post not found!');
                    alert('Post not Found!\n\nReloading page!');
                    location.reload();
                }, 2000);
            }
        }
    }
}

// This function is used to hide the option (create new post or edit old post) selector.
function hide_option_selector()
{
    document.getElementById('page-head-id').style.animation = 'hide-card 2s forwards 1';
    document.getElementById('page-head-id').addEventListener('animationend', () => {
        document.getElementById('page-head-id').style.animation = '';
        document.getElementById('page-head-id').style.display = 'none';
    });
}

// This function listens for changes in the input field for file upload.
// It displays the name of the file selected.
function display_file_name()
{
    // Displays the selected file's name block.
    document.getElementById('file-to-upload-name-container').style.display = 'block';

    // Display the selected file's name.
    const selected_file_to_upload = document.getElementById('file-upload-input').files;
    const file_to_upload_display_name = selected_file_to_upload[0].name;
    document.getElementById('selected-file-name-display').innerText = file_to_upload_display_name;
}
