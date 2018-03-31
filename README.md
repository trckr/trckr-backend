# trckr-backend
The backend of the trckr application

## Getting Started

* Start the project and run the containers in detached mode `sudo docker-compose up -d`
* Run db migrations `sudo docker-compose run web python manage.py migrate`
* (optional) Create an admin user `sudo docker-compose run web python manage.py createsuperuser`
* Visit `http://localhost:8000` and admin area at `http://localhost:8000/admin`

