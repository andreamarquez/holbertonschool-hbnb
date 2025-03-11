## TASK 0 (Requirement included on the task 0 for the README file):
In the README.md file, write a brief overview of the project setup:
a) Describe the purpose of each directory and file.
b) Include instructions on how to install dependencies and run the application.


### Instructions

#### Dependencies
To install the dependencies (flask and the REST extension) use:
```
pip install -r requirements.txt
```

#### Test the Initial Setup

To check the available endpoints
```
flask routes
```

To run the application to ensure everything is set up correctly:
```
flask run
```
The app will be running on: `http://localhost:5000`

You can interact with the endpoints on: `http://localhost:5000/api/v1/`

#### Running tests
How to run the tests (be sure you are inside part2 directory):
```
pytest
```


### API Endpoints

| Endpoint                    | Methods           | Rule                              |
|-----------------------------|-------------------|-----------------------------------|
| amenities_amenity_list      | GET, POST         | /api/v1/amenities/                |
| amenities_amenity_resource  | DELETE, GET, PUT  | /api/v1/amenities/<amenity_id>    |
| doc                         | GET               | /api/v1/                          |
| places_place_list           | GET, POST         | /api/v1/places/                   |
| places_place_resource       | DELETE, GET, PUT  | /api/v1/places/<place_id>         |
| reviews_place_review_list   | GET               | /api/v1/reviews/places/<place_id> |
| reviews_review_list         | GET, POST         | /api/v1/reviews/                  |
| reviews_review_resource     | DELETE, GET, PUT  | /api/v1/reviews/<review_id>       |
| users_user_list             | GET, POST         | /api/v1/users/                    |
| users_user_resource         | DELETE, GET, PUT  | /api/v1/users/<user_id>           |

--------------------------------------------------------------------------
