## Project Name: Insta Clone
## Author: Daniel Muthama
## Technologies Used
1. Django
2. Html
3. Css
4. Bootstrap 5

## set up and installation
* clone the project to your local machine
* Install project requirements with the following command:

    * pip3 install -r requirements.txt
* Configure the database of choice: Either Sqlite or Postgresql
* create a .env file in the root project folder and include all the secret keys.
* Make sure all your keys are accessible in the setting.py file by writing the following commands:

    1. set -o allexport
    2. source .env
    3. echo $SECRET_KEY
* Create the admin username by:

    * python3 manage.py createsuperuser
* run the project by:

    * python3 manage.py runserver

## License MIT
Copyright(c){2022}{Crispus Njenga} Permission is hereby granted, free of charge, to any person obtaining a copy of this project. The person can clone to add any specification that meets his or her requirements.

MIT ©2022 Daniel Muthama