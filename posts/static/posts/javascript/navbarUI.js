/*
    Copyright (C) 2019 OM SANTOSHKUMAR MASNE. All Rights Reserved.
    Licensed under the GNU Affero General Public License v3.0 only (AGPL-3.0-only) license.
    See License.txt in the project root for license information.
*/

document.addEventListener("DOMContentLoaded", startup);


// This function sets the necessary styling to be displayed when the page is loaded.
function startup()
{
    document.getElementById('user-dropdown').style.display = 'none';
    document.getElementById('user-icon').addEventListener('click', toggle_user_options);
}

// Listens for clicks on the user icon button and toggles the displaying of the user dropdown.
function toggle_user_options()
{
    var dropdown = document.getElementById('user-dropdown');
    if(dropdown.style.display == 'block')
    {
        dropdown.style.display = 'none';
    }
    else
    {
        dropdown.style.display = 'block';
        dropdown.style.animation = 'dropdown-stack 0.5s forwards 1';
        dropdown.addEventListener('animationend', () => {
            dropdown.style.animation = '';
        });
    }
}

// When the user clicks anywhere outside the user icon button, the dropdown is removed from the viewport.
window.onclick = function(e){
    if(!(e.target == document.getElementById('user-icon-img'))){
        if(document.getElementById('user-dropdown').style.display == 'block')
        {
            document.getElementById('user-dropdown').style.display = 'none';
        }
    }
}
