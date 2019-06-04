Django React Chat Example Project
=================================

An example project showing a chat app with Django Channels, 
Webpack, React and Docker.


## Assumptions
1. Unix shell commands are given below. 
   Windows likely will need some work but is left as an exercise to the 
   user.


## Prerequisites
1. Install Docker for your system so that `docker-compose` and `docker`
   are available from the command line.   
2. Install [`nvm`](https://github.com/nvm-sh/nvm) and make sure that 
   `~/.nvm/nvm.sh` has been sourced in your `~/.bash_profile`.
3. Use `nvm` to install the version of node supported by this project: 
   `nvm install`. After it's installed, run `nvm use`. Both of these 
   commands will utilize the version in the `.nvmrc` file.
4. Install `yarn` package manager. `npm` likely works, too but was
   not tested.
5. Ensure you are in the `django-react-chat/django_react_chat_example_project` directory


## Installation
1. `export COMPOSE_FILE=local.yml` - if you don't do this, you'll have to 
   add `-f local.yml` to all `docker-compose commands below
2. `yarn install` - install the javascript packages
3. `yarn dev` - start generating the webpack bundle
4. `docker-compose build` - compile the Docker Images,
   using the docker-compose file at `local.yml`. 
   - This may take some time, especially if this is the first time you 
     have used docker with python.
   - This runs a pip install when compiling the docker image. 
5. `docker-compose up` - Run the compiled docker images.
6. configure a postgres client
   - in pycharm, I use a Postgres Database connection:  
   - the password is blank
   - the username and database are both 
     `django_react_chat_example_project`
   - This is configured in the docker-compose `local.yml` file
   - ![postgres db config](docs/postgres_db_connection_pycharm.png)
7. create a superuser
   - `docker-compose run django python manage.py createsuperuser`
8. run http://localhost:8000/ in your web browser
   - create two users either using the sign up process, or using the `/admin` django admin
   - Use Chrome to create two different users, and try logging in with each user in different chrome space
   - Use the django admin to set the email address for both users as verified
   - If you prefer, you can also do this last part using postgres client instead of using the django admin. 
     Open the `django_react_chat_example_project.public.account_emailaddress` table and set the `verified` 
     bit to true and confirm.
     - optional: you can also do this from the command line client using 
       `docker-compose -f local.yml run postgres`, but this is left 
       as an exercise for the user
   - go to `http://localhost:8000/` signed in as both users
   - chat!
   - ![chat screenshot](docs/chat_example.png)
   

## Useful commands
* `$ docker-compose run django python manage.py migrate`
  * `./manage.py migrate` is called during 
    `docker-compose up`, but useful to know anyway
