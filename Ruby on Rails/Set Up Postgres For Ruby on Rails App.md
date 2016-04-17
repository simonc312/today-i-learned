# Setting Up Postgres For Ruby on Rails App 
## On Linux 

Check out basics on [Digital Ocean's guide](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-14-04)

1. Install 

	sudo apt-get update
	sudo apt-get install postgresql postgresql-contrib 

2. Log in as default superuser. May need to set a password.

	sudo postgres -u psql

3. Create test and staging databases 

	> CREATE DATABASE your\_app\_test\_db 

4. Create new user and make it owner of new databases 

	> CREATE USER new_user WITH PASSWORD password
	
	> ALTER DATABASE your\_app\_test\_db OWNER new_user

5. View info on your databases and users 

    > \l # for databases
    
    > \du # for users
    
    > \q # quit psql command prompt
    
    > \? # psql help 
    
    > \h # postgres help 

6. Set up rails db config file located in config/database.yml

    default: &default
        
        adapter: postgresql
        
        encoding: utf8
        
        user: username
        
        password: ENV['password'] 
        
        host: localhost
        
        port: 5432

    development:
        
        <<: \*default
        
        database: your\_app\_dev\_db

    test:
        
        <<: \*default
        
        database: your\_app\_test\_db

7. Create migrations and update schema or insert seed data

