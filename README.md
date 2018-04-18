# trckr-backend
The backend of the trckr application

## Getting Started

* Start the project and run the containers in detached mode `docker-compose up -d`
* Run db migrations `docker-compose exec web python manage.py migrate`
* (optional) Create an admin user `docker-compose exec web python manage.py createsuperuser`
* Visit `http://localhost:8000` and admin area at `http://localhost:8000/admin`

