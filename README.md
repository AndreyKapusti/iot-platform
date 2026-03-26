# Geting started
To start fastapi app (windows):
- cd path\to\repo\back
- make venv
- venv\scripts\activate (to activate venv)
- make install
- make dev (to start docker with postgre and fastapi app)  

If you already started dev (make dev), you can stop fastapi app by cntr+C, but decker app will continue to work. You can run fastapi app only by "make run", because docker already launched. If you need to stop docker container you can use "make docker-down". To run only docker-compose up" use "docker-compose up" or "make docker-up".