# A Multi User Blog

#### Created by: John Laine

## [Demo](https://udacity-muli-user-blog.appspot.com/)

## Description
A multi user blog written in Python that utilizes the App Engine platform by Google.

This project was created and submitted to Udacity as part of the Full Stack Developer Nanodegree program.

## Running the Application
1. Install the [Google Cloud SDK](https://cloud.google.com/sdk/downloads), installation will vary depending on your system.
2. Clone the project to your local machine: `clone https://github.com/johnlaine1/udacity-fsnd-blog.git`
3. cd into the project `cd udacity-fsnd-blog`
4. Depending on your system setup, you may be able to just run `dev_appserver.py app.yaml` from the root directory of the project (where the app.yaml file is located) and view the app at http://localhost:8080/ <br>
If this does not work for you, I am sorry and please find more information about `dev_appserver.py` [here](https://cloud.google.com/appengine/docs/python/tools/using-local-server)
## Using the Application
1. All posts can be viewed on the front page by both logged in or anonymous users.
2. Click 'Login or Register' to login or create a new account.
3. Anyone can **view** posts and comments, only registered users can **create** posts and comments
4. Logged in users can create posts, comments and 'like' other users' posts, they can also edit thier own posts and comments. Users cannot like thier own posts.
5. Click on 'Create New Post' to create a post.
6. While viewing a post, click on 'Add a Comment' to add a comment to the post 
7. While viewing a post, click on the 'Like' button to like the post. The 'Like' button will then change to 'Unlike', which you can click again to unlike the post.
8. While viewing a post or a comment, click on edit or delete to edit or delete the post.