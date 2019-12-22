/*
    Copyright (C) 2019 OM SANTOSHKUMAR MASNE. All Rights Reserved.
    Licensed under the GNU Affero General Public License v3.0 only (AGPL-3.0-only) license.
    See License.txt in the project root for license information.
*/

document.addEventListener('DOMContentLoaded', startup);

// This function displays a message via an alert to the user.
// This message is embeded by the server on the page, if any.
// It waits for sometime before displaying the message to the user.
function startup()
{
    setTimeout(() => {
        message = document.getElementById('message').value;
        if(message != 'false')
        {
            alert(message);
        }
    }, 1000);
}
