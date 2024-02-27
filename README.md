# BUHREC: Streamlining School Project Management
BUHREC is a user-friendly and comprehensive web application designed to simplify the creation, management, and review of school projects. It empowers students, researchers, reviewers, and administrators to collaborate effectively throughout the project lifecycle.

## Technologies Used
### Frontend
    - HTML
    - CSS
    - JavaScript
### Backend
    - Django

## Key Features
1. **Versatile User Roles**: Choose from four distinct roles: Student, Researcher, Reviewer, and Admin. Each role comes with tailored functionalities to ensure a smooth workflow.
2. **Streamlined Project Management**: Students and researchers can effortlessly create, edit, and delete their projects, gaining full control over their project journey.
3. **Comprehensive Review Process**: Reviewers can thoroughly examine assigned projects, providing valuable feedback through approvals, disapprovals, and detailed remarks.
4. **Efficient Administration**: Admins, specifically Chair and Assistant Chair, play a crucial role in managing the overall process. Chair admins can assign and withdraw reviewers, while assistant chair admins can allocate automatic track IDs for each project.
5. **Seamless Integration**: BUHREC seamlessly integrates with existing school systems, ensuring a smooth transition into your current infrastructure.

## Actions
### Geberal user actions
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
4. Create a `media` folder in the root directory of the project as well.

### OPTIONAL
You can create a virtual environment before running the commands in number 2.

#### Creating the Virtual Environment
- Open your terminal or command prompt.
- Navigate to the directory where you want to create your virtual environment.
- Execute the following command:
    `python -m venv /path/to/new/virtual/environment`
- Replace /path/to/new/virtual/environment with the desired location for your virtual environment. For example:
    `python -m venv .venv`
- This will create a virtual environment in the current directory.
- On Windows, you can also use the following command:
    `python -m venv c:\path\to\myenv`

#### Activate the Virtual Environment
After creating the virtual environment, activate it:
- On Windows:
    `.venv\Scripts\activate`

- On macOS/Linux:
    `source .venv/bin/activate`

#### Deactivate the Virtual Environment
When you’re done working in the virtual environment, deactivate it:
    `deactivate`