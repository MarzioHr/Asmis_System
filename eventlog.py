import dbconnection
from datetime import datetime

# set DB cursor
mycursor = dbconnection.mydb.cursor()

def connectLogDB():
  try:
    mycursor.execute("USE eventlog")
  except:
    print("MySQL connection failed.")

def createSearchLog(user_id,table,attribute,value):
  dtNow = datetime.now()
  datestamp = dtNow.strftime("%d/%m/%Y %H:%M:%S")
  connectLogDB()
  sql = "INSERT INTO events(datetime, operation, user_id, used_table, attribute, search_value) VALUES(%s,%s,%s,%s,%s,%s)"
  val = (datestamp, "search", user_id, table, attribute, value) 
  mycursor.execute(sql, val)
  dbconnection.mydb.commit()
  return True

def createEditLog(user_id,table,attribute,edit_id,old,new):
  dtNow = datetime.now()
  datestamp = dtNow.strftime("%d/%m/%Y %H:%M:%S")
  connectLogDB()
  sql = "INSERT INTO events(datetime, operation, user_id, used_table, attribute, edited_id, old_value, new_value) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
  val = (datestamp, "edit", user_id, table, attribute, edit_id, old, new)
  mycursor.execute(sql, val)
  dbconnection.mydb.commit()
  return True