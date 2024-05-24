## Backend online installation


pip install flask-cors Flask Flask-JWT Flask Flask-JWT-Extended flask flask-sqlalchemy Flask Flask-Bcrypt flask_cors


## Backeng alembic and migration instructions
 - If you have deleted the alembic folder, then follow the following steps:

     pip install alembic

     alembic init alembic

     alembic revision --autogenerate -m "description_of_migration"

     alembic upgrade head 


 - if you haven't deleted the folder:
    alembic revision --autogenerate -m "description_of_migration"
    alembic upgrade head

