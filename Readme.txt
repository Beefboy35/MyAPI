This fancy API was developed by me in two evenings, You can use it as a sample for creating standard API stuff(registration, authorization using jwt access token, even simple localization is realised).
All standard methods (post, get ,delete, put) are implemented, so you can have fun playing with them, i used postgresql as a database storage.
This API doesn't work with SwaggerUI, i don't know why, so i used Postman to test it instead.
Before using it make sure you've set the URL of your database in db.connection.py and alembic.ini files, Have fun! (One more thing, i used alembic to create another column in the table)
