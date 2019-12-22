/*
    Copyright (C) 2019 OM SANTOSHKUMAR MASNE. All Rights Reserved.
    Licensed under the GNU Affero General Public License v3.0 only (AGPL-3.0-only) license.
    See License.txt in the project root for license information.
*/

var current_stage = 0;
var stage_list = ['stage-one', 'stage-two', 'final-stage'];

var username, password, confirm_password, email, first_name, last_name;

document.addEventListener("DOMContentLoaded", startup);

// Sets the necessary conditions, when the page is loaded.
function startup()
{
    console.log("SIGNUP JS STARTED!");

    username = document.getElementById('username');
    password = document.getElementById('password');
    confirm_password = document.getElementById('confirm_password');
    email = document.getElementById('email');
    first_name = document.getElementById('first_name');
    last_name = document.getElementById('last_name');

    set_stage('stage_one');
    document.getElementById('return-button').addEventListener('click', stage_back);
    document.getElementById('form-next-btn').addEventListener('click', next_stage);
    document.getElementById('form-submit-btn').addEventListener('click', submit_form);
    username.addEventListener('blur',check_username);
}

// Validates the form and submits it upon successful validation.
function submit_form()
{
    let check_status = check_stage('final-stage');
    if(!check_status)
    {
        setTimeout(function() {
            alert('Please check your form.');
        }, 1000);
        return false;
    }
    document.getElementById('signup-form').submit();
}

// Checks if the username chosen by the user is available or not.
function check_username()
{
    var status = false;
    const request = new XMLHttpRequest();
    const data = new FormData();
    data.append('username', username.value);
    request.open('POST', '/api/check-username/');
    request.send(data);
    request.onload = () => {
        const data = request.responseText;
        if(data)
        {
            data_recieved = JSON.parse(request.responseText);
            if(!data_recieved.username_availability)
            {
                alert('Username is not available!\n\nPlease choose different username.');
                username.value = '';
                status = false;
                set_stage('stage-one');
            }
        }
    }
    return status;
}

// Sets the previous stage according to the stage list.
function stage_back()
{
    if(current_stage > 0)
    {
        set_stage(stage_list[current_stage - 1]);
    }
}

// Sets the next stage according to the stage list.
function next_stage()
{
    let check_status = check_stage(stage_list[current_stage]);
    if(!check_status)
    {
        return false;
    }

    if(current_stage < 2)
    {
        set_stage(stage_list[current_stage + 1]);
    }
}

// Sets the selected stage.
function set_stage(new_stage_name)
{
    let stage_one = document.querySelector('.stage-one');
    let stage_two = document.querySelector('.stage-two');
    let final_stage = document.querySelector('.final-stage');
    let next_btn = document.querySelector('#form-next-div');
    let submit_btn = document.querySelector('#form-submit-div');
    let back_btn = document.querySelector('#return-button');
    switch(new_stage_name)
    {
        case 'stage-one':
            stage_one.style.display = 'block';
            stage_one.style.animation = 'stage-start 1s forwards 1';
            stage_one.addEventListener('animationend', () => {
                stage_one.style.animation = '';
            });

            stage_two.style.display = 'none';

            final_stage.style.display = 'none';

            next_btn.style.display = 'block';
            next_btn.style.animation = 'Btn-introduce 1s ease 1';
            next_btn.addEventListener('animationend', () => {
                next_btn.style.animation = '';
            });

            submit_btn.style.display = 'none';
            back_btn.style.display = 'none';
            current_stage = 0;
            break;

        case 'stage-two':
            stage_one.style.display = 'none';

            stage_two.style.display = 'block';
            stage_two.style.animation = 'stage-start 1s forwards 1';
            stage_two.addEventListener('animationend', () => {
                stage_two.style.animation = '';
            });

            final_stage.style.display = 'none';

            next_btn.style.display = 'block';
            next_btn.style.animation = 'Btn-introduce 1s ease 1';
            next_btn.addEventListener('animationend', () => {
                next_btn.style.animation = '';
            });

            submit_btn.style.display = 'none';

            back_btn.style.display = 'block';
            back_btn.style.animation = 'Btn-introduce 1s ease 1';
            back_btn.addEventListener('animationend', () => {
                back_btn.style.animation = '';
            });

            current_stage = 1;
            break;

        case 'final-stage':
            stage_one.style.display = 'none';

            stage_two.style.display = 'none';

            final_stage.style.display = 'block';
            final_stage.style.animation = 'stage-start 1s forwards 1';
            final_stage.addEventListener('animationend', () => {
                final_stage.style.animation = '';
            });

            next_btn.style.display = 'none';

            submit_btn.style.display = 'block';
            submit_btn.style.animation = 'Btn-introduce 1s ease 1';
            submit_btn.addEventListener('animationend', () => {
                submit_btn.style.animation = '';
            });

            back_btn.style.display = 'block';
            back_btn.style.animation = 'Btn-introduce 1s ease 1';
            back_btn.addEventListener('animationend', () => {
                back_btn.style.animation = '';
            });

            current_stage = 2;
            break;

        default:
            stage_one.style.display = 'block';
            stage_two.style.display = 'none';
            final_stage.style.display = 'none';

            next_btn.style.display = 'block';
            submit_btn.style.display = 'none';
            back_btn.style.display = 'none';
            current_stage = 0;
    }
    return true;
}

// Shakes the corresponding element.
function shake_element(element_name)
{
    element_name.style.animation = 'Shake 1s forwards 1';
    setTimeout(function() {
        element_name.style.animation = '';
    }, 1000);
}

// Validates the stages (form elements).
function check_stage(stage_name)
{
    let check_status = true;
    switch(stage_name)
    {
        case 'stage-one':
            if(username.value == '')
            {
                shake_element(username);
                check_status = false;
            }
            if(password.value == '')
            {
                shake_element(password);
                check_status = false;
            }
            break;

        case 'stage-two':
            if(confirm_password.value != password.value)
            {
                alert('Password is not matching.\n\nPlease type password again.');
                confirm_password.value = '';
                shake_element(confirm_password);
                check_status = false;
            }
            break;

        case 'final-stage':
            if(email.value == '')
            {
                shake_element(email);
                check_status = false;
            }
            if(first_name.value == '')
            {
                shake_element(first_name);
                check_status = false;
            }
            if(last_name.value == '')
            {
                shake_element(last_name);
                check_status = false;
            }
            break;
        default:
            check_status = false;
            console.log('Error checking page!');
    }
    return check_status;
}
