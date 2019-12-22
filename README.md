# Project 4 : UNVERSE!

## Web Programming with Python and Javascript

# This project has been created by ***OM SANTOSHKUMAR MASNE*** .

### Created on 20/10/2019.
### All dates mentioned in this project are in the format: DD/MM/YYYY.

### This website is a project website created for EDX course, Web Programming with Python and JavaScript.

### This is an web-app for Posts sharing - UNIVERSE.

---

### USAGE:

#### Requirements:

* Install the necessary requirements: `pip install -r requirements.txt`.

#### SAFETY CHECKS:

* Check the `settings.py` file in `universe` directory.

#### DATABASE SETUP:

* Setup the database by using the following commands in the project root directory:
1. `python manage.py makemigrations`.
2. `python manage.py migrate`.

#### SETUP ADMIN:

* Run the following commands:
1. `python manage.py createsuperuser`.
2. Follow on screen instructions.

#### Running the server (app):

* Type these commands in the terminal from the project root directory:
    * `python manage.py runserver`.

---

### The website's functions as described below:

* This project is a website for sharing posts and stories.

* The '/' route lands the user at the homepage.

* The recently submitted posts are displayed on the homepage.

* If the user is not logged in, then, options for login and signup are shown to the user.

    * The user has to register to create and submit posts to the website.

    * The user may register by using the SIGNUP button on the homepage. This will open the signup form.

    * Once the user is registered successfully, the user is redirected to the website homepage. If there are problems in registration, then a error page is shown.

    * The user can login to his account using the LOGIN button available at the homepage.

* Once logged in, the user can check his profile and also has options to manage his posts and logout.

* On the profile page, the user can check his name, email id, and username and may also check his old posts.

* On manage posts section, the user may create a new post or edit an old one.

    1. The user may upload a plain text file or a markdown file to create his post.

    2. Alternatively, the user may write his post directly in the web-app.

    3. The posts can be edited via the web-app, by selecting the post title and using the edit option.

* Before final submission, a post preview is shown, and option is given to user to submit it or cancel it.

* Submitted posts can be viewed through 2 links:

    1. The post link : `/post/<author_name>/<post_title>/`.

    2. The post direct link (permanent link) : `/post-direct/<post-id>/`.

A footer is also shown on index (homepage) page, displaying the name of the creator of this project and short information about the project.

Many other HTML and CSS properties are used in this project website to enhance its appearance.
This project website is also compatible with devices with small screens (screen resolution).

---

### OTHER NOTES:

* Users created without using signup form cannot submit any posts (Eg. Admin account created from terminal).

* They have to create the custom user's model object and then, they will be able to submit posts.


---

### This project uses [DJANGO](https://www.djangoproject.com).

### This project uses [BOOTSTRAP](https://getbootstrap.com).

### Background [Photo](https://unsplash.com/photos/CIKB91GrL1Y) by [Darren Lawrence](https://unsplash.com/@wild_away) on [Unsplash](https://unsplash.com/).

### This project uses MediumEditor: [website](https://yabwe.github.io/medium-editor/), [MediumEditor github](https://github.com/yabwe/medium-editor).
### MediumEditor licensed under the MIT license.

---

## License:
### Licensed under the GNU Affero General Public License v3.0 only (AGPL-3.0-only) license.
### Copyright (c) 2019 OM SANTOSHKUMAR MASNE. All Rights Reserved.
