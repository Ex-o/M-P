## Environment
- Python 3.8
## Database
- Postgres@14
- psycopg2 python driver
## Server
- Flask dev env
## Running steps
`export FLASK_APP=main.py` \
`flask run`
### Request example 
```curl -X POST -F "name=khaled" -F "type=user" -F "email=test@gmail.com" -F "country=Egypt" -F "address=Innopolis, Russia" -F "phone=+1234567" http://127.0.0.1:5000/adduser```
## Testing
- pytest