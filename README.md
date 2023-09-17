# Customer-Ordering-System Api

A customer ordering system built using Django rest framework and deployed on an AWS ec2 instance. 

- Link to the deployed app and endpoints: 

  http://ecom.sarahnjuguna.com/

- Read more about the endpoints and path parameters:

    http://ecom.sarahnjuguna.com/redoc/

-  Link to the logic flow:

    https://www.figma.com/file/sk6mNq8OGN6gJTmMKSWtHb/Customer-ordering-user-flow?type=whiteboard&node-id=0%3A1&t=z2EpbytIW2HzHGVY-1

   ## ERD diagram:

   ![ERD with colored entities (UML notation)](https://github.com/Sarah358/Customer-Ordering-System/assets/60597568/594e7c9c-f162-4c05-ae54-7187079a6008)

  
## Basic features

### 1. Authentication and authorization
- User creates an account and verifies the account using OTP sent to their phone numbers
- User login involves generating a token which is set as a cookie and can be passed on the header to authorize the user
- Users can update their profile information and view their details
- Users can also log out and the authorization token is revoked

### 2. Products and categories 
- Admins can add products and categories to the system
- Users can view all available products and filter products by product name, category name, or both

### 3. Orders and order items 
- Users can create orders and add products to the orders specifying the quantity
- The system ensures the order quantity is not greater than the stock
- The user gets the total cost of their orders and the order items in an order
- The user can also filter orders using the order status

### 4. Checkout 
- Users can checkout a pending order
- The system sends an SMS to the user with the reference code of the order and the total cost
- The system then sets the order status to placed

## Technologies Used
1. Django Rest Framework
2. PostgreSQL
3. Celery and redis
4. Docker and Docker compose 
5. Nginx and Gunicorn
6. Twilio
7. AWS,ec2 and rds
8. Drf spectacular, Swagger UI, and redoc
9. Pre-commits,flake8,isort ,and black
10. Pytest, and test coverage
11. CI/CD - GitHub actions and Gitstream

## Getting Started 
Clone this repository to your local machine

``` 
https://github.com/Sarah358/Customer-Ordering-System.git
```

Rename the ```.env.example``` file found in the project's root directory to ```.env``` and update the environment variables accordingly.

Ensure you have docker and docker-compose installed and use the following commands to build and run your containers.

```
docker compose up --build -d --remove-orphans
docker compose exec api python3 manage.py migrate

```
Locate the ```Make``` file in the project's root directory for the other commands used in the project. Commands include running ```tests``` and ```test coverage```

Navigate to ``` http://localhost ``` to view the project API endpoints documentation.

#### Preview of the documentation UI

![image](https://github.com/Sarah358/Customer-Ordering-System/assets/60597568/2fc4c60f-76fb-4e27-aaa7-e98fdcc4a04b)

### Pre- Commits and linters
- pre-commits ensure clean code and prevent one from committing code that is not well formatted.
- It also prevents one from committing to the main branch. check the ```.pre-commit-config.yml``` file in the project's root directory for available hooks.

### Git Workflow and CI/CD simulation

- The project's development and deployment process is managed through a CI/CD pipeline.
-  When changes are committed to the main branch, a series of deployment tasks are triggered.
-  These tasks involve:
  
    1.  connecting to the server
    2.  fetching the latest updates from the main branch,
    3.  rebuilding Docker containers,
    4.  performing database migrations,
    5.   running tests, and confirming that all tests pass successfully.
       
-  Once these tasks are successfully completed, the jobs are marked as successful.

  ![CICDpipeline-1](https://github.com/Sarah358/Customer-Ordering-System/assets/60597568/7a7408c2-1948-4be6-9a7f-a61bd60a14ff)


### Gitstream

-  Additionally, I have added Gitstream which automates how code gets merged from the individual to the main branch with a clear set of repo-level rules.
  
  1. Adding context to every PR, like Estimated Time to Review
  2. Automatically assigning the right reviewer and number of reviewers to PRs
  3. Code review automation that auto request changes
  4. Automating PR Approvals & Merges

## Deployment 
The app is deployed on an AWS ec2 instance and rds for the database as earlier mentioned. 

The process for deployment involved:

1. Creating an ec2 instance on AWS and generating ```.pem``` file.
2. SSH into the server using the pem file.
2. Install the required software which includes docker and docker-compose.
3. Creating an RDS database instance and configuring its security group settings.
4.  After setting up the instances, I cloned the project from Git Hub and built the containers.
5.  Finally, I added the ec2 logging credentials on the GitHub actions file to enable automation in development, testing, and deployment.

   You can access the deployed project here:    http://ecom.sarahnjuguna.com/







  
