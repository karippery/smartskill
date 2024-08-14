# Smart-Skill
Project Name: Smart skill

Platform: Django

Description: This is a web application designed to streamline the process of employee skill management within a company. With a large number of employees, it can be challenging for a company to identify the perfect candidate for a new project. This application aims to solve this problem by providing a platform to store and manage employee skills and skill levels.



### Run the Server:

run the development server to make sure everything is set up correctly:

python manage.py runserver

System check identified no issues (0 silenced).
August 10, 2024 - 15:47:18
Django version 4.2, using settings 'core.settings'
Starting development server at http://127.0.0.1:8090/
Quit the server with CTRL-BREAK.

### Migrate the Database
Apply the migrations to create the database tables:


python manage.py makemigrations
python manage.py migrate

## Login system
The application will feature a JWT token-based login system to ensure secure access. The data will be organized into several tables: