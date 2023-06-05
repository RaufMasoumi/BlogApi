# BlogApi
## _Anything you need in your blog!_
![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/RaufMasoumi/BlogApi?color=important&logo=python&logoColor=yellow) ![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/RaufMasoumi/BlogApi/django?color=orange&logo=django) ![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/RaufMasoumi/BlogApi/djangorestframework?color=green) ![GitHub last commit](https://img.shields.io/github/last-commit/RaufMasoumi/BlogApi?color=brightgreen&logo=github)

BlogApi is a perfect sample RESTful API project that has been written using the Django and of course Django Rest Framework.
The goal of this project is to give you all the requirements for building a responsive blog web application using modern front-end frameworks like [React JS](https://reactjs.org/).

You can name BlogApi as:
- Reliable
- Ease-to-use
- Secure
- Neat
- Clean
- Comprehensible

The primitive idea of this project is from [Django For APIs](https://djangoforapis.com/) book.

The project has been deployed to Back4App and you can experience it at [BlogApi Back4App](https://blogapi1-raoufrm93.b4a.run/).

As this is a perfect backend project, the requests of the front-end developers for collaboration are gladly accepted.


## Features

- Allowing CRUD functionality for each endpoint.
- Easy-to-use endpoints.
- Ordered, paginated and clean data.
- Secure authentication method.
- Comprehensible endpoint addresses.
- Dynamic content negotiation.
- Hyperlinked data.
- Filterable, searchable and orderable.
- Well tested.

The back-end and front-end cooperation balance has been always a challenge; As it is possible to build a project with 70% work in back-end and 30% work in front-end and vice versa; But in this project, the goal is to provide all the front-end requirements and serve the data in a way that no need to touch them at all.


## Tech

BlogApi uses all of these technologies to being a stable and reliable backend:

- [Python](https://www.python.org/) - A powerful, high-level and popular programming language.
- [Django](https://www.djangoproject.com/) - An enormous Python-based backend web framework.
- [DRF](https://www.django-rest-framework.org/) - A strong and flexible Django-based framework for building web APIs.
- [PostgreSQL](https://www.postgresql.org/) - A powerful, open source object-relational database system.
- [Back4App](https://www.back4app.com/) - A container as a service platform.
- [Neon](https://neon.tech/) - A database as a service platform.

By assembling all of these technologies in one place for making an idea real, BlogApi now has a heart of Python that pumps the power throughout the project, a body of Django providing ability to move, and magic of DRF to talk to you and make you happy!


## Backend

By choosing Django and DRF for building the backend of this project, BlogApi has a lot of things that wishes to say you about its backend. let's talk about them!
BlogApi has two django apps such as:
- Account - For user accounts and providing the authentication features.
- Posts - The main app that is handling the posts, comments, etc functionality.


### Models

It has five different models to organize the database:
- CustomUser - A custom user model overriding Django's AbstractUser model.
- Tag - To use in posts' hashtags.
- Post - The main model for blog posts.
- Comment - For post comments.
- Reply - For comment replies.

Also thanks to the Django model indexes, using Post model is more optimised.


### Serializers

A big difference of a django API project with the normal one is they have serializers for getting and converting the data from client and sending the correct data to it.

BlogApi has a lot of serializers for handling the complexity of the coming data and serving a neat, easy-to-read and beautiful response. Also thanks to the DRF's nested serializers and applying it in the project, now the responses are more understandable because the relationships of elements will be close to your eyes, and you can access them more easily.

The Hyperlinked serializers is a topic that BlogApi persists on it! Most of the data that you get, especially the data with some relations, have hyperlinks to access the elements much more easily than before.

Another interesting point about the serializers of the project is a model may do not have one serializer but multiple serializers for serving data. The advantage of this topic is when your going from a list view to a more specific view like a detail view, the data will change and will zoom further into the element, according to the view depth! For example if you look at a post list view, you will not get much data about the author of the post but if you go to the post detail view, you will see the author's username and of course the profile url thanks to the nested serializers.

Also, if you see a serializer data with beauty, but you are a little confused in sending that data, you should not worry about it because you don't need to send the data that way but the normal data that you are comfortable with those; After that the serializer itself will make it more beautiful for you. In short BlogApi's serializers are getting the normal data and sending the most beautiful data!


### Views

As same as the other Django apps, BlogApi has lots of different views; But the new and exciting thing is almost all of that views are not the normal Django views, they are DRF's API views that provide RESTful API architecture!

Almost all the views provide full CRUD functionality and support get, post, put, patch and delete requests.

In this project, the django class based views have been preferred instead of function based views because of :

- Inheritance
- Easy-to-understand
- Avoiding the errors
- Up-to-date
- Less code


Regardless of the models' normal list and detail views, there is a specific importance in this project on the relationships -as there is a base custom generic view class exactly for these relations-. There are many views for the elements' normal and of course reverse relations. For example if a post has comments, in addition to being able to see some shorted data of them in list and detail views of the posts, there is a route like "/posts/1/comments/" that you can see all the post's comments.

Thanks to using Django's authentication system the reverse relation views related to the users are much easier to use, because if you have logged in, you don't need to use this path pattern: "/users/{your_pk}/posts" to see your posts, you can just simply go to: "/users/posts/" and you will see your posts again. 


#### ViewSets and Routers

Django Rest Framework in addition to the normal API views, provides some ViewSets and Routers. It allows you to combine the logic for a set of related views in a single class, called a ViewSet. In the other hand, the Rest framework adds support for automatic URL routing to Django, and provides you with a simple, quick and consistent way of wiring your view logic to a set of URLs, called a Router.

One of the subjects that makes BlogApi self-confidently happy is: It's using some ViewSets and Routers to automate the tasks!

For now the viewsets and routers have been used more often for the posts and users, but with growing the project up and mounting some related view logics, the amount of them will be increased.


### Authentication

When it comes to use an API, the authentication system would be more important for both the client and the server, and exactly for this reason BlogApi does not stay in the defaults and tries to use the maximum features of Django and DRF!

Because the authentication issues are serious issues, so it would be a good practice to not code them personally and rely on some third-party projects that exactly focused on those topics.

BlogApi uses DRF's Token Authentication system for its APIs where each client has its token and will be using it in each request. And in the same time the Rest framework uses Session Authentication for its browsable API views.

In the other hand and regardless of the browsable authentication views that DRF provides them, BlogApi uses [Django Allauth](https://django-allauth.readthedocs.io/en/latest/installation.html) and [Dj Rest Auth](https://dj-rest-auth.readthedocs.io/) packages for supporting the authentication APIs (like login and logout APIs).

By assembling all of these stuffs' powers in one system, now BlogApi has a secure and reliable authentication system that supports a perfect account cycle!


### Permissions

Permissions as a way to restrict unexpected users' accesses to the sensitive data, is helping the server to be more calm about what type of users will access to a specific endpoint.

With having a good authentication system, having a good permission system is accessible.

BlogApi has some generic permission classes that is using them in almost all the views; It means the aggressor users will not be able to do anything they want.
A good instance of permissions' marks on this project is the users' posts issues: Suppose that you have created a new post, and you are happy that nobody can change your new-created post; But oops!! An aggressor user changed your post very easily! And exactly in this position BlogApi turns the time over and its permissions would be there to preserve your post and prevent bad users!


### Throttling

Maybe you logged out a site, but you have forgotten your password. Probably you will be testing tons of passwords to find the correct one; But after some requests you might be getting a message like this: "You are sending too many requests!" That is exactly the thing that called the "Throttling" in Django. This topic is more important in APIs and is helping to handle issues like:
- Stopping the aggressor users.
- Reducing the unnormal amount of requests.
- Keeping the system safe and strong.

BlogApi is using some throttling classes that are restricting too many requests sent by unauthenticated, and in a few positions by the authenticated users.

Combining a great authentication, permission, and throttling systems together, provides a safe and calm environment both for the clients and the server.

Maybe you are a little worry about: Wow! how many restrictions exist in this project. But BlogApi is doing all of these things for you and ensures you that you will not be molested with these policies, and they will affect only on the aggressor users.

### Searching, Ordering and Filtering
As a costumer of an API service provider, you might always consider at least one touch on the data that you receive. Some of the duties that you might think of them to do yourself, are: searching, ordering and filtering the data. The downside of this issue is you should write more codes and the "more codes" means more time!

In this project you will not need to change the data at all; Because the endpoints of BlogApi allow related query parameters to cary that duties themselves!

The query parameters are available everywhere you might need to.


#### Searching

If you want to search through a specific word(s), you can easily just send the "search" query parameter assigned to thing that you want to search; And you can see all the related data of your searched subject.

For example if you wish to search the posts by "Django" keyword, the address should change from:
```sh
"/posts/"
```
 to
 
 ```sh
 "/posts/?search=Django"  
```


#### Ordering

If the default ordering of the data that you receive is not the preferred one, you can use "ordering" query parameter assigned to the specific field of elements; And you will get the new-ordered data which you imagined.

For example if you want to order the posts by the "created_at" field, the address should change from:
```sh
"/posts/"
```
 to
 
 ```sh
 "/posts/?ordering=created_at"  
```


#### Filtering

If you are looking for some specific and related data inside a lot of the other data, you can find them by filtering the data using elements' field names as a query parameter assigned to thing that you want to filter by.

For example if you want to filter posts by their title containing "Django Rest Framework" without case sensitivity, the address will change from:
```sh
"/posts/"
```
 to
 
 ```sh
"/posts/?title__icontains=Django+Rest+Framework"
```

BlogApi for supporting the filtering in endpoints, is using [Django Filter](https://django-filter.readthedocs.io/) package's filter backend and has some FilterSet classes to enable the fields' filtering.


### Pagination

It is always common to get a lot of data, and you feel lost! But in this project there is another very useful option named "Pagination".

BlogApi has a default pagination in all of its endpoints but if you wish, you can customize it by sending related query parameters.

For example if you want to see the first page of 10-element-paginated posts, the address should change from:
```sh
"/posts/"
```
 to
 
 ```sh
"/posts/?page=1&page_size=10"
```
Thanks to the DRF's next and previous hyperlinks, browsing through paginated data is easier than ever!


### Schemas

An API schema is like a database schema definition but for APIs, to make integration between platforms easier for developers. 

BlogApi for supporting the API schemas endpoints, uses [DRF Spectacular](https://drf-spectacular.readthedocs.io/) package.

There are three different endpoints for schemas:
- /api/schema/ - For downloading the schema file.
- /api/schema/redoc/ - A Redoc-generated schema view.
- /api/schema/swagger-ui/ - A Swagger-generated schema view.

Also, The schema file is available in the project's source code too.


### Tests
"Code without tests is broken as designed." Everyone in the Django community knows this very well; But the tests are a part of projects that often times developers ignore doing it because of the tests are not affecting the project itself; But it is much better to test your project with the tests, not manually yourself. Also, if you want to show to someone that your project works without any problem, better to show your project tests' result.

BlogApi has almost 50 tests that are testing the whole project. Till here, you discovered a lot of different parts of BlogApi, and maybe you named them a "part" of project; But it would be better to name them as a "well-tested part" of project; Because There are multiple tests for each of them.

If you wish to run the tests and see the result, please go to the [Running Tests](#running-tests) part.


## Docker
Docker is a platform that use OS-level virtualization to deliver software in packages called containers. One of the best advantages of docker is that it makes building, deploying and testing processes of the project very easy and comfortable; So as a developer who wants to test some project locally you really don't need to do any extra thing than lifting the project's docker container up.

BlogApi now supports docker and uses docker compose for dockerizing the project itself and the Postgres database for the best experience.

In the [Installation](#installation) section you will see that how easy is testing BlogApi.


## Installation
As BlogApi supports docker, so running the project in development can be done in two ways: You can install and run the project with docker or just using the traditional alternative way.

If you are not comfortable with docker you can pass docker installation and go to the [alternative installation](#alternative-installation) section. 

BlogApi as a django project in the first step needs Python; So first install it.

### Docker installation
The first thing that you need in using a dockerized project, is the Docker itself. So in the start you have to install the Docker Desktop.

If you are using Mac, you can install Docker Desktop from [Installing Docker Desktop in mac](https://docs.docker.com/desktop/install/mac-install/);

Or if you are using Windows, you should go to [Installing Docker Desktop in windows](https://docs.docker.com/desktop/install/windows-install/).

#### Launching Docker Compose
Docker Compose is a tool that helps to define multi-container docker applications much easier. With Compose, we can create a YAML file to define the services and with a single command, can spin everything up or tear it all down.

We will use docker compose to have the BlogApi and [PostgreSQL](https://www.postgresql.org/) together for best experience.

The first step is creating a docker compose file for local development; As we have docker-compose-production.yml file so making the one that is suitable for local development is easy.

Also, for using django projects you must have a secret key; so we will generate a new one.

On Mac using Bash Shell execute:
```sh
cd BlogApi
touch docker-compose.yml
```
on Windows Command Prompt run:
```sh
cd BlogApi
type nul > docker-compose.yml
```

And then generate the secret key using the command below and copy it:
```sh
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

After that, copy all lines of docker-compose-production.yml file into new-created docker-compose.yml file.

And then add the environment variables, below the only variable that exists and replace your new-generated secret key:
```sh
...
environment:
  - DATABASE_URL=postgresql://raufmasoumi:secret@postgres:5432/BlogApi
  # New environment variables
  - DJANGO_SECRET_KEY=YOUR NEW-GENERATED SECRET KEY
  - DJANGO_DEBUG=True
  - DJANGO_SECURE_SSL_REDIRECT=false
  - DJANGO_SECURE_HSTS_PRELOAD=false
  - DJANGO_SECURE_HSTS_SECONDS=0
  - DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=false
  - DJANGO_CSRF_COOKIE_SECURE=false
  - DJANGO_SESSION_COOKIE_SECURE=false
...
```

That's it! let's go to run the containers.


#### Running the containers
Now we are ready to run the project with docker compose. To spin up the containers, just run:
```sh
docker compose up --build
```

And then migrate the migrations:
```sh
docker compose exec app python manage.py migrate
```

Open your browser at:
```sh
127.0.0.1:8000
```
or
```sh
localhost:8000
```

And finally you can see the BlogApi's home page!


### Alternative installation
If you don't wish to use docker, you can just install the project using the traditional way.

First we will create a python virtual environment; There are many choices to do that but in this project for increasing comfort, [Pipenv](https://pipenv.pypa.io/) has been chosen.

First step is installing Pipenv itself:

```sh
cd BlogApi
python -m pip install pipenv
```

Then just simply install dependencies from Pipfile and finally start a Pipenv shell to activate the virtual environment:

```sh
pipenv install 
pipenv shell
```


#### Development

Now you are ready to run the project in your local server.

First you need to create a .env file to your project level directory, so you can set the environment variables for development, because the variables' defaults were set for production environment for security reasons.

On Mac using Bash Shell: 
```sh
touch .env
```
On Windows using the Command Prompt: 
```sh
type nul > .env
```

Then generate a new django secret key:
```sh
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy variables below to .env and replace your secret key:
```sh
DJANGO_SECRET_KEY=YOUR NEW-GENERATED SECRET KEY
DJANGO_DEBUG=true
DATABASE_URL=sqlite:///db.sqlite3
DJANGO_SECURE_SSL_REDIRECT=false
DJANGO_SECURE_HSTS_PRELOAD=false
DJANGO_SECURE_HSTS_SECONDS=0
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=false
DJANGO_SESSION_COOKIE_SECURE=false
DJANGO_CSRF_COOKIE_SECURE=false
```

Migrate the migrations and finally lift server by executing runserver command:
```sh
python manage.py migrate
python manage.py runserver
```
Open your browser at:
```sh
127.0.0.1:8000
```
or
```sh
localhost:8000
```

and you will see BlogApi's home page!


### Running Tests
To run the project tests, just execute:
```sh
python manage.py test
```
Or if you are using dockerized version:
```sh
docker compose exec app python manage.py test
```


## License
This project is licensed under the terms of the GNU General Public license.



**Rauf Masoumi**
