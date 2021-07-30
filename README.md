## Linux Ubuntu setup

    sudo apt-get update
    sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl

#### Creating the PostgreSQL Database and User

    sudo -u postgres psql
Create database:

    CREATE DATABASE myproject;
    
    CREATE USER myprojectuser WITH PASSWORD 'password';

    ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
    ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
    ALTER ROLE myprojectuser SET timezone TO 'UTC';

    GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;

#### Creating virtual environment

    sudo -H pip3 install --upgrade pip
    sudo -H pip3 install virtualenv

    mkdir ~/myprojectdir
    cd ~/myprojectdir


**Within the project directory, create a Python virtual environment by typing:**

    virtualenv myprojectenv
Activate environment:

    source myprojectenv/bin/activate

**Clone project from github**

    git clone https://github.com/prowsandy/django-blog
Open project directory

    cd django-blog

Install requirements

    pip3 install -r requirements.txt

Migrate Database

    python3 manage.py migrate

Run server

    python3 manage.py runserver

Seed data by browsing:

    http://127.0.0.1:8000/seed

---
**API Docs**
#### Features
#### 1. User Signup

    HTTP Method: POST 
    URL: api/auth/signup

##### Request Body

-   `email`  - user’s email
-   `password`  - user’s password
-   `name`  - user’s name

#### 2. User Login

    HTTP Method: POST 
    URL: api/auth/login 
    Headers: - Authorization: "Token {encodedusername:password}"
##### Request Body

-   `email`  - user’s email
-   `password`  - user’s password

#### 3. Create Post

    HTTP Method: POST 
    URL: api/post 
    Headers: - Authorization: "Token {token}"
##### Request Body

-   `title`  - blog title
-   `content`  - blog content

#### 4. Update Post

    HTTP Method: PUT 
    URL: api/post/:id 
    Headers: - Authorization: "Token {token}"
##### Request Body

-   `title`  - blog title
-   `content`  - blog content

#### 5. Delete Post

    HTTP Method: DELETE 
    URL: api/post/:id 
    Headers: - Authorization: "Token {token}"
#### 6. Retrieve Logged-in User’s Posts

    HTTP Method: GET 
    URL: api/me/posts 
    Headers: - Authorization: "Token {token}"
#### 7. Retrieve All Posts

    HTTP Method: GET 
    URL: api/posts
#### 8. Retrieve Single Post

    HTTP Method: GET 
    URL: api/posts/:id
#### 9. Create Comment

    HTTP Method: POST 
    URL: api/posts/:post_id/comments 
    Headers: - Authorization: "Token {token}"
##### Request Body
-   `content`  - comment content

#### 10. Delete Comment

    HTTP Method: DELETE 
    URL: api/posts/:post_id/comments/:id 
    Headers: - Authorization: "Token {token}"
#### 11. Retrieve Post Comments

    HTTP Method: GET 
    URL: api/posts/:post_id/comments
