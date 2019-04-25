# E-commerce Buildup App

[![Coverage Status](https://coveralls.io/repos/github/Maxcutex/personal_ecommerce/badge.svg?branch=develop)](https://coveralls.io/github/Maxcutex/personal_ecommerce?branch=develop)
[![CircleCI](https://circleci.com/gh/Maxcutex/personal_ecommerce.svg?style=svg)](https://circleci.com/gh/Maxcutex/personal_ecommerce)

This is an application to build and e-commerce app. 


## Usage
Using  Python download and install the latest version of Python 3+.

The application is built with Python

To clone the respository execute the following command.
```
git clone https://github.com/maxcutex/personal_ecommerce.git
```
Navigate into the cloned project directory.

Edit the `env-sample` file with your gmail credentials and save it as `.env`

Change the parameters in there to your own settings.

The key ```FLASK_APP``` must be set to ```run```. The value of the`APP_ENV` between 

`development` and `testing` in order to run the application `development` or `testing` 

mode respectively.

On the prompt execute the following 
```
export $(cat .env)
```


Execute the following code to install all the application dependencies.
```
python install -r requirements.txt
```

Execute the following code to migrate all data tables/object
```
python run.py db migrate
```


Execute the following at the command line
```
python run.py runserver
```

Browse the application in the url
```
http://localhost:5000
```

### Features of E-commerce App
- View administrative functionality
- View products
- Make purchases
- Add to shopping cart



### Testing
Tests can be run using
```
pytest
```