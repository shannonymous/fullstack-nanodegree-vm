# Item Catalog Project

A content management system, developed using the Flask framework in Python. Authentication is provided via OAuth and all data is stored within a PostgreSQL database. Authenticated users will have the ability to Edit and Delete owned items. Authenticated users will be able to create new items.

## Tools and Frameworks
This web application was built with HTML5, CSS, Vagrant, Flask, SQLAlchemy and Google Oauth2 & APIs.

## Instruction
To run the web application:
1. Install Vagrant and Virtual Box
2. Clone [this repository](https://github.com/shannonymous/fullstack-nanodegree-vm)
3. Launch the Vagrant VM (in the *vagrant* folder directory  from the terminal) with the command:
`vagrant up`
4. Access the shell with:
`vagrant ssh`
5. Navigate to the *catalog* directory:
`cd /vagrant/catalog`
6. From directory */vagrant/catalog*, initialize the application database and generate rows in the database with the following two commands:
`python database_setup.py`
`python sportsgen.py`
7. You are now ready to run the catalog program. Run:
`python application.py`
7. Access the application by visiting http://localhost:8000 on your broswer of choice.
