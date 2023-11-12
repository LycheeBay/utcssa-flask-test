import os
import psycopg2
from  datetime import datetime, timezone
from dotenv import load_dotenv
from flask import Flask,request

CREATE_ROOM_TABLE = (
    "CREATE TABLE IF NOT EXISTS rooms (id SERIAL PRIMARY KEY, name TEXT);"
)
CREATE_TEMPS_TABLE ="""CREATE TABLE IF NOT EXISTS temperatures (room_id INTEGER, temperature REAL,
                        date TIMESTAMP, FOREIGN KEY(room_id) REFERENCES rooms(id) ON DELETE CASCADE);"""
INSERT_ROOM_RETURN_ID = "INSERT INTO rooms (name) VALUES (%s) RETURNING id;"
INSERT_TEMP = (
    "INSERT INTO temperatures (room_id, temperature, date) VALUES (%s,%s,%s);"
)
GLOABAL_NUMBER_OF_DAYS = (
    """SELECT COUNT(DISTINCT DATE(date)) AS days FROM temperatures;"""
)
GLOBAL_AVG = """SELECT ACG(temperature) As average FROM temperatures;"""

load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

@app.get("/")
def index():
    return "Hello World"


# Api 1 Checkin: check if email is recorded 
#  receive a string conatin email address
#  check email address format
#  filter sql
#  check response
#  send to front end
@app.post("/api/checkin")
def create_room():
    data = request.get_json()
    name = data["name"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_ROOM_TABLE)
            cursor.execute(INSERT_ROOM_RETURN_ID, (name,))
            room_id = cursor.fetchone()[0]
    return {"id":room_id,"message":f"Room {name} created."},201

# Api 2 Checkin: return display
#  receive a string conatin email address
#  filter sql
#  check response, withdraw data from response
#  send to front end
@app.post("/api/temperature")
def add_temp():
    data = request.get_json()
    temperature = data["temperature"]
    room_id = data["room"]
    try:
        date = datetime.strptime(data["date"], "%m-%d-%Y %H:%M:%S")
    except KeyError:
        date = datetime.now(timezone.utc)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_TEMPS_TABLE)
            cursor.execute(INSERT_TEMP, (room_id,temperature,date))
            Ename= cursor.fetchone()[0]
            Lottery_id= cursor.fetchone()[1]
    return {"Ename":Ename,"Lottery_id":Lottery_id },201


# Api 3 Lottery: lottery status
#  filter sql, return array
#  process response, generate random number
#  send to front end
@app.get("/api/average")
def get_global_avg():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GLOBAL_AVG)
            average = cursor.fetchone()[0]
            cursor.execute(GLOABAL_NUMBER_OF_DAYS)
            days = cursor.fetchone()[0]
    return {"average": round(average,2),"days":days}


# Api 4 Lottery: save winner
#  receive a string lottery number
#  insert sql, (response)
#  check response, withdraw data from response
@app.post("/api/average")
def get_global_avg():
    data = request.get_json()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GLOBAL_AVG)
            average = cursor.fetchone()[0]
            cursor.execute(GLOABAL_NUMBER_OF_DAYS)
            days = cursor.fetchone()[0]
    return {"average": round(average,2),"days":days}
