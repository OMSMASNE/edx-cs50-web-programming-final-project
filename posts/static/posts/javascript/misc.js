/*
    Copyright (C) 2019 OM SANTOSHKUMAR MASNE. All Rights Reserved.
    Licensed under the GNU Affero General Public License v3.0 only (AGPL-3.0-only) license.
    See License.txt in the project root for license information.
*/

document.addEventListener('DOMContentLoaded', startup);

// This function checks if a new_account_status message is present or not.
// If message is found, the cancel and go to homepage link's innerText is changed.
// Else a message is printed on the console.
function startup()
{
    try
    {
        message = document.getElementById('new_account_status').value;
        if(message == 'true')
        {
            document.getElementById('cancel-and-go-back-link').innerText = 'Goto HomePage!';
        }    
    }
    catch (error)
    {
        console.log('New account message not found.');
    }
}
