# Fiszkly

## Participants 
 - Michał Leszczyński - Team Leader
 - Tomasz Rajchel
 - Anna Malik
 - Dominik Trybuch
 - Stanisław Tęczyński

### Do you need more people: No

## Short description of the idea

Fiszkly is a web application that helps you broaden your vocabulary by creating a personal training plan with flashcards.
You simply add the list of words you’d like to learn and then practice them until you know them by heart.

## Features:
- sign in/ sign up
- user ranking
- custom word lists created and shared by users
- flashcards rarity levels
- adding custom words (list)
- progress charts & other analytics
- notifications (eg. you missed your daily challenge)
- achievements, daily bonuses
- social media integration

# Local development
requirements:
* docker
* docker-compose

There are two containers:
* fiszkly_web - hosts the Django app and is defined in the Dockerfile.
* fiszkly_db - hosts the database and is based on the postgres docker image.

You can start the containers by running
```
docker-compose up -d
```
This will start the containers in detached mode.

To see the logs from those containers use the command
```
docker-compose logs -f
```

To execute commands in any of those containers use
```
docker exec -ti <container_name> bash
```

There are two volumes that are accessible both from the host system and within the containers
* .:/code - the whole catalog 'Fiszkly' is mounted inside the web container which means that you don't have to restart the containers whenever you make a change to the code.
* ./db:/var/lib/postgresql/data - the db catalog is mounted inside the db container to allow persistent storage of your local database. So you can stop and even remove the containers and the data will still be there.


To access your local database enter the db container and run the interactive postgres terminal
```
docker exec -ti fiszkly_db bash
psql postgres postgres
```