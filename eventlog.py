import dbconnection
from datetime import datetime # python lib to query date and time

# set DB cursor
mycursor = dbconnection.mydb.cursor()

def connectLogDB():
  """
  Function to connect to the 'eventlog' database.
  """
  try:
    mycursor.execute("USE eventlog")
  except:
    print("MySQL connection failed.")

def createSearchLog(user_id:int, table:str, attribute:str, value:str) -> bool:
  """
  Function to create a search event log entry in the database.
  Takes as input the user_id that actioned the event, the table in which the search was conducted ('patients'/'appointments'),
  the attribute which was search (e.g. patient's first name or date of birth) and the exact search term that was entered.
  """
  dtNow = datetime.now()
  datestamp = dtNow.strftime("%d/%m/%Y %H:%M:%S") # captures datetime of when the function was called
  connectLogDB()
  sql = "INSERT INTO events(datetime, operation, user_id, used_table, attribute, search_value) VALUES(%s,%s,%s,%s,%s,%s)"
  val = (datestamp, "search", user_id, table, attribute, value) 
  mycursor.execute(sql, val)
  dbconnection.mydb.commit()
  return True

def createEditLog(user_id:int, table:str, attribute:str, edit_id:int, old:str, new:str) -> bool:
  """
  Function to create an edit event log entry in the database.
  Takes as input the user_id that actioned the event, the table in which the edit was conducted ('patients'/'appointments'),
  the attribute which has been changed (e.g. patient's first name or date of birth), the id of the row that is being edited,
  the previous value prior to the change, and the new value that is being saved.
  """
  dtNow = datetime.now()
  datestamp = dtNow.strftime("%d/%m/%Y %H:%M:%S")
  connectLogDB()
  sql = "INSERT INTO events(datetime, operation, user_id, used_table, attribute, edited_id, old_value, new_value) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
  val = (datestamp, "edit", user_id, table, attribute, edit_id, old, new)
  mycursor.execute(sql, val)
  dbconnection.mydb.commit()
  return True