# IS211_FinalProject
This project is a web application that provides users with the ability to create, view, edit, and delete blog posts. The application is built using the Python programming language and the Flask web framework. It uses a SQLite database to store blog posts and user account information.

To use the application, you will need to have Python and the Flask web framework installed. Once you have cloned the project repository, you can run the app.py file to start the application. The application can be accessed in your web browser at "http://localhost:5000".

There are two user accounts included in the application: bob and alice. You can log in to either of these accounts using the password "password1" or "password2", respectively.

The database has two tables: one for user accounts and one for blog posts. The user accounts table includes fields for the user's ID, username, and password. The blog posts table includes fields for the post's ID, title, content, publication date, and author ID. The author ID is a foreign key that represents the user ID from the user accounts table.

When you click on the "Create Post" button, the application uses SQLite to execute SQL commands that insert the new post data into the blog posts table. This data can then be viewed by the user in the application.
