# Welcome to the Enjoy Cooking API
 
## About the Enjoy Cooking API
This API allows users to search for recipes and save them in their favourites.  
To use the API, a user needs to register and log in.  
Then a user can search for recipes by:  
    - ingredients they are want to use to prepare a meal,  
    - optionally a dish they plan to prepare.  
Results of a search are displayed with:  
    - a title of a recipe,  
    - a URL of a recipe,  
    - list of ingredients needed.  
A user can save a recipe to their favourites by providing the following:  
    - a title of a recipe (required),  
    - a URL of a recipe (required),  
    - list of ingredients needed (required),  
    - category (optional),  
    - comment (optional).  
A user can view all their favourites recipes or a particular one.  
They can also update or delete their favourites.   
  
An admin has more privileges:  
    - to view users stats,
    - to view recipes stats,  
    - to delete any user from db.

## User authorization and authentication
A user is authorized by providing their username and password. 
A user is authenticated by access_token or refresh_token (JWT claims).

## Database information
The database consists of 3 tables:  
    - a users table,  
    - a recipes table,  
    - a favourite_recipes table - which joins users and recipes by many-to-many relationship and has some additional fields.    
Recipes are identified by their unique URLs and/or ids.  
A particular recipe can be saved to the recipes table only once - it is identified by its URL.  
Users are identified by their unique ids and/or unique usernames.  
There are 2 types of users: regular users (admin=0) and admins (admin=1).  
Admins are more privileged than regular users (e.g. can see stats, can delete any user).   
A user can save a particular recipe only once. After that they can update it or delete it.

## How to prepare environment and run the Enjoy Cooking API
I used Python 3.8.1. and Flask 1.1.2 to build this RESTful API.  
You need to install all the frameworks and libraries I used to write it   
(you can find them listed in the requirements.txt file).  
Then you'll need to find and use your EXTERNAL_API_KEY:  
    1. to get your EXTERNAL_API_KEY:  
        - log in to <https://rapidapi.com/>,   
        - search for Recipe Puppy API and open it,  
        - look for a "X-RapidAPI-Key" textbox - this is your EXTERNAL_API_KEY.    
    2. create an external_api_key.py file (for details open the external_api_key.py.example I've provided),  
    3. paste your EXTERNAL_API_KEY to your external_api_key.py file.  
Finally, run the app by double-clicking app.py.  
  
You can use Postman to check all the endpoints. I've included my Postman collection in the postman_collection folder.

## Info about the source of data used in the API
The Enjoy Cooking API connects to another API to get the data it needs. 
To find that awesome external API:  
    1. log in to <https://rapidapi.com/>,  
    2. search for Recipe Puppy API (created by brianiswu - thanks brianiswu!). 