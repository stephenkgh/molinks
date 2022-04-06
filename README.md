Overview
========

This project is a simple web application for saving bookmarks made with
Django, Postgres and Docker.  It's really just a toy project but the
goal was to try some things:

- making a Django project secure by default (see below)
- integrating a Django/Docker project with an external nginx webserver
  (via uwsgi)
- making the project work in a sub-path of an existing website with no
  knowledge of the path
- using faker to generate test data
- handling user-selectable themes
- creating a simple and quick Javascript search feature

Secure by default
-----------------

This project requires a login and each user has their own collection of
data not visible to other users.  The challenge was to do this at the
model level so that each view doesn't need to worry about isolating user
data from other users.

This was a little challenging.  It seems Django wasn't designed to work
like this and instead expects this kind of concern to be handled at the
view level.  The problem with that approach is that you have to think
about security every time you make a new view, which is easy to forget
about and can lead to data breaches.


Installing
==========

*Note:* This has only been tested under linux.  You'll need GNU make
installed because a makefile has been horribly abused to help simplify
docker commands.  (Before I did this I was constantly mixing up dev and
prod arguments to docker and causing problems...)


Docker
------

Docker Compose V2 is needed for following this guide.  I used the following
to install docker locally:
- follow https://docs.docker.com/engine/install/ubuntu/
- follow https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user
- make sure `docker-compose` is *not* installed
- install compose cli command by following https://docs.docker.com/compose/cli-command/


Dev
---

To get a dev instance of this project running locally on your machine
do the following:

    make up build
    make init       # will ask some questions to make a Django super-user
    make test

Then go to http://localhost:8000/ in your web browser and log in as the
super-user account.  Also, to see what the project looks like when filled
out with some data do this:

    make fakeuser

Login with the new account then scroll to the bottom and change the
theme to "L33t NeRD".  This will reveal the quick search box - try it out!


Prod
----

This guide is for installing under a traditional (ie. non-containerized)
webserver.  Django and Postgres will still be in their containers but
Django will communicate with an external nginx process.  You'll need a
webserver running nginx (with the uwsgi module) and docker.

### nginx config ###

You'll need to add 2 location blocks to your nginx config:

```
    location /molinks/static {
        rewrite ^(/molinks/static)/(.*) /molinks-static/$2 last;
        return 403;
    }

    location /molinks {
        include         snippets/uwsgi-params.conf;
        uwsgi_pass      127.0.0.1:8000;
        uwsgi_param     SCRIPT_NAME /molinks;
    }
```

Change "molinks" above to whatever sub-path you want the project to
appear under.  Also, `snippets/uwsgi-params.conf` points to a copy of
this file: https://github.com/nginx/nginx/blob/master/conf/uwsgi_params


### Postgres password ###

(This project uses an environment variable for the Postgres password;
not ideal but that's as far as I got.)  Create the file `etc/secrets.env`
and set a secure password:

    cp etc/secrets.env.example etc/secrets.env

*NOTE*: To make sure these secrets are never accidentally added to git
add the following to the `.git/info/exclude` file:

    etc/*
    !etc/*.example


### Docker context ###

The Makefile assumes the existence of a Docker context named `prod`
for installing to the production server.  Set it up like this:

    docker context create prod --description "production server" --docker "host=ssh://username@example.com"


### Static files ###

Django doesn't serve static files through uswsgi (ie. images, css,
javascript).  You need to install these in a separate location on your
webserver and reference them in the nginx config above.

The Makefile uses rsync to copy the files to your webserver but needs to
know where.  This is determined by the two make variables `REMOTE_HOST`
and `REMOTE_STATIC` which can be set in etc/custom.mk:

    cp etc/custom.mk.example etc/custom.mk

After editing that file do:

    make staticfiles


### Start it up ###

Once the above is all set you start the containers almost the same as in dev mode:

    make prod up build
    make prod init
    make prod test


Other notes
===========

There are a bunch more helpful docker shortcuts in the Makefile.  See the code for
details but here are a few examples:

    make ps
    make shell
    make dbshell
    make log tail
    make down clean

Here's a more complete `.git/info/exclude` file to use for this project:

    etc/*
    !etc/*.example
    homedir/*
    !homedir/.placeholder
    staticfiles/

