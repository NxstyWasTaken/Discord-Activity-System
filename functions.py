import sqlite3,math 
db = sqlite3.connect("main.sqlite")
cursor = db.cursor()
class NxstyFunctions:
    def __init__(self):
        print("Nxsty Init")
    def dbsetup():
        cursor.execute('''CREATE TABLE IF NOT EXISTS activity(userid int,hours int,minutes int,seconds int)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS temp_data(userid int,time int)''')
    def convert(diff):
        hours = math.floor(diff /3600000) % 24
        minutes = math.floor(diff / 60000) % 60
        seconds = math.floor(diff / 1000) % 60   
        return hours,minutes,seconds
    def getleaderboard(size): #Broken.....
        cursor.execute("SELECT * FROM activity ORDER BY hours DESC , minutes DESC , seconds DESC;")
        data = cursor.fetchmany(size)
        leaderboard = []
        for i in range(len(data)):
            leaderboard.append(data[i])
        return leaderboard
    def getactivity(user):
        cursor.execute("SELECT * FROM activity WHERE userid = {user}".format(user=user))
        data = cursor.fetchone()
        return data
    def get_temp_data(user):
        cursor.execute('SELECT * FROM temp_data WHERE userid = {user}'.format(user=user))
        results = cursor.fetchone()
        return results
    #db things
    def updateuser(user,data,time):
        data = data
        convert = NxstyFunctions.convert(time)
        cursor.execute("UPDATE activity SET hours={hours},minutes={mins},seconds={secs} WHERE userid = {id}".format(hours=data[1]+convert[0],mins=data[2]+convert[1],secs=data[3]+convert[2],id=user))
        db.commit()
    def insertuser(user,time):
        convert = NxstyFunctions.convert(time)
        cursor.execute("INSERT INTO activity (userid,hours,minutes,seconds) VALUES({id},{hours},{mins},{secs})".format(id=user,hours=convert[0],mins=convert[1],secs=convert[2]))
        db.commit()
