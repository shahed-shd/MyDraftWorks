REST API Test
================

### `POST /users`
#### Request: 
    {
        "firstName": <firstname>,
        "lastName": <lastname>,
        "password": <password>
    }
#### Response: 
##### Status: `<Use Appropriate Status Code>`
    {
        "id": <id>
    }

### `GET /users/{id}`
#### Response:
##### Status: `<Use Appropriate Status Code>`
    {
        "id": <id>
        "name": <full name> 
    }


### `POST /users/{id}/tags`
#### Request:
    {
        "tags": [<tag 1>, <tag 2>, ...],
        "expiry": <miliseconds>        
    }
#### Response:
##### Status: `<Use Appropriate Status Code>`
    {}



### `GET /users?tags=<tag1>,<tag2>`

#### Response:
##### Status: `<Use Appropriate Status Code>`
    {
        "users": [
            {
                "id": <id 1>
                "name": "<full name 1>"
                "tags": [<tag 1>, <tag 2>, ...]
            },
        ]
    }
    
