# BUHREC
This is a school project management application built with Django that makes creation and management of school projects easy for all parties involved like the students, project reviewers, and school admins. The application is easily integrated into school systems as well.

## Features
### User
- Creating account where they can select one of four roles which are Student, Researcher, Reviewer, and Admin
- Setting up profile based on the role selected.
- Login
- View account details
- Update details like name, email, password

### Student and Researcher
- Create project
- Edit project
- Delete project
- View project details

### Reviewer
The reviewers get assigned a project by the admin and once they are assigned a project, they can do the following:
- View project
- Approve and unapprove project
- Make remarks on project

### Admin
As an admin, two roles are involved:
- Chair admin
- Assistant chair admin

    #### Chair admin
    - View all projects
    - Assign reviewer to a project
    - Withdraw reviewer from a project

    #### Assistant chair admin
    - View all projects
    - Assign automatic track id to a project

## Set up on local machine
1. Clone the project by using the command in the terminal: `git clone https://github.com/joboy-dev/BUHREC-Project.git`
2. Run the following commands:
    #### Windows
    - `pip install -r requirements.txt` to get the necessary dependencies
    - `py manage.py makemigrations` to have a database file
    - `py manage.py migrate`
    - `py manage.py collectstatic` which is essential for the ck5editor used in the project
    - `py manage.py runserver` to start up the develeopment server

    #### Mac
    - `pip install -r requirements.txt` to get the necessary dependencies
    - `python3 manage.py makemigrations` to have a database file
    - `python3 manage.py migrate`
    - `python3 manage.py collectstatic` which is essential for the ck5editor used in the project
    - `python3 manage.py runserver` to start up the develeopment server
3. Create a `.env` file in the root directory of the project and add a `SECRET_KEY` variable:
    `SECRET_KEY = 'random characters'`

#### OPTIONAL
You can create a virtual environment before runningthe commands in number 2.