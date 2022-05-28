SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "StackOverflow-lite",
        "description": "A Demo for the StackOverflow-lite api in flask",
        "version": "0.1.1",
        "contact": {
        "name": "Smith Ringtho",
        "email": "sringtho@gmail.com",
        }
    },
    "securityDefinitions": {
        "Bearer": 
        {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. " +  
            "Example: \"Authorization: Bearer {token}\""
        }
  },
  "security": [
    {
      "Bearer": [ ]
    }
  ]
}