import mysql.connector

mydb = mysql.connector.connect(
    host="192.168.4.112",
    user="root",
    password="password",
    database="bank"
)
cursor = mydb.cursor()
sql = "INSERT INTO users (username) VALUES (%s)"
val = (["admin"])
cursor.execute(sql, val)
mydb.commit()

proceed = input("do 2")

cursor.execute("SELECT * FROM users")
result = cursor.fetchall()
print(result)

proceed = input("do 3")


sql = "UPDATE users SET password = %s WHERE username = %s"
val = ("password", "admin")
cursor.execute(sql, val)
mydb.commit()

proceed = input("do 4")


sql = "DELETE FROM users WHERE username = %s"
val = ("hamo4260",)
cursor.execute(sql, val)
mydb.commit()

cursor.close()
mydb.close()