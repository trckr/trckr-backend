# trckr-backend
The backend of the trckr application

## Getting Started

* Start the project and run the containers in detached mode `sudo docker-compose up -d`
* Run db migrations `sudo docker-compose run python3 manage.py migrate`
* (optional) Create an admin user `sudo docker-compose run python3 manage.py createsuperuser`
* Visit `http://localhost:8000` and admin area at `http://localhost:8000/admin`

