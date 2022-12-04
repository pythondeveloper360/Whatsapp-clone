from json import dumps
from random import shuffle

from psycopg2 import connect, sql

database = connect(host='localhost', database='whatsapp', user='postgres',
                   password='pos-72270', port=5432)

cursor = database.cursor()


def tokenGenerator(_range=10):
    alphabet = [*[chr(i) for i in range(ord('a'), ord('z')+1)], *[chr(i)
                                                                  for i in range(ord('A'), ord('Z')+1)], *[str(i) for i in range(0, 10)]]
    shuffle(alphabet)
    return ''.join(alphabet[0:_range])


def authUserLogin(username, token, client_id):
    sqlquery = sql.SQL('select user_id from logins where {username} = %s and {token} = %s and {client_id} = %s').format(
        username=sql.Identifier("user_id"),
        token=sql.Identifier("token"),
        client_id=sql.Identifier("client_id")
    )
    cursor.execute(sqlquery, (username, token, client_id))
    response = cursor.fetchone()
    return True if response else False


def authUser(username, password):
    sqlquery = sql.SQL('select id from users where {username} = %s and {password} = %s ').format(
        username=sql.Identifier("id"),
        password=sql.Identifier("password")
    )
    cursor.execute(sqlquery, (username, password))
    response = cursor.fetchone()
    return True if response else False


def loginUser(username, password, date):
    if authUser(username=username, password=password):
        token, client_id = tokenGenerator(), tokenGenerator()
        sqlquery = sql.SQL('insert into logins({date},{user_id},{token},{client_id}) values(%s,%s,%s,%s)').format(
            date=sql.Identifier("date"),
            user_id=sql.Identifier("user_id"),
            token=sql.Identifier("token"),
            client_id=sql.Identifier("client_id")
        )
        cursor.execute(sqlquery, (date, username, token, client_id))
        database.commit()
        return {"auth": True, "token": token, 'client_id': client_id}
    else:
        return False


def getChats(user_id):
    sqlquery = sql.SQL('select * from rooms where {participants} = any(%s)')


def getUserDetails(user_id):
    sqlquery = sql.SQL('select * from users where id = %s')
    cursor.execute(sqlquery, (user_id,))
    respone = cursor.fetchone()
    if respone:
        return {'name': respone[1], 'email': respone[2]}
    return False


def createRoom(user_id, _date,room_name):
    userDetails = getUserDetails(user_id=user_id)
    if userDetails:
        room_id = tokenGenerator()
        sqlquery = sql.SQL(
            "insert into rooms ({room_id},{date},{participants},{room_name},{particpants_list}) values(%s,%s,%s,%s,%s)").format(
                room_id = sql.Identifier("room_id"),
                date = sql.Identifier("date_created"),
                participants = sql.Identifier("participants"),
                room_name =sql.Identifier("room_name"),
                particpants_list = sql.Identifier("participants_list")
            )
        cursor.execute(sqlquery, (room_id, _date, dumps({'participants': [
                       {'name': userDetails['name'], 'id':user_id, 'email':userDetails['email']}]}),room_name,[user_id]))
        database.commit()
