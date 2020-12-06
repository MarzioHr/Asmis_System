import eventlog
import dbconnection

# set DB cursor
mycursor = dbconnection.mydb.cursor()

def connectDataDB():
  """Function to connect to the 'data' database for subsequent search query and patient/appointment edit capability"""
  try:
    mycursor.execute("USE data")
  except:
    print("MySQL connection failed.")
    
def searchPatient(attribute, value, uid):
  eventlog.createSearchLog(uid,"patients",attribute,value)
  connectDataDB()
  mycursor.execute("Select * FROM patients WHERE %s = '%s'" % (attribute,value))
  result = mycursor.fetchall()
  resultCount = len(result)
  if resultCount == 0:
    print("No results found, please try again.")
    return
  elif resultCount > 0:
    print("Found a total of %s result(s):" % resultCount)
    print("----------------------------------------------------------------------------------------")
    for i in range(0,resultCount):
      print("ID: %s\t Name: %s %s\t Date of Birth: %s\t Consultant ID: %s" % (result[i][0], result[i][1], result[i][2], result[i][3], result[i][4]))
  print("\n Please choose an option:")
  print(" 1.) Edit patient record")
  print(" 2.) Return to main menu")
  while True:
    userSelect = input("\nPlease choose an option: ")
    if userSelect == "2":
      return
    elif userSelect == "1":
      editRecord = input("\nPlease enter the ID of the patient you want to edit: ")
      editPatient(editRecord, uid)
      return
    else:
      print("Invalid selection. Please check your input and try again.")

def editPatient(patient_id,uid):
  connectDataDB()
  print("\n What attribute do you want to edit?")
  print(" 1.) Patient's first name")
  print(" 2.) Patient's last name")
  print(" 3.) Patient's date of birth")
  print(" 4.) Cancel")
  selectionLoop = True
  while selectionLoop == True:
    editRecord = input("\nPlease enter the ID of the patient you want to edit: ")
    validResponse = ("1","2","3","4")
    if editRecord == "4":
      return
    elif editRecord in validResponse:
      selectionLoop = False
    else:
      print("Invalid selection. Please check your input and try again.")
      
  if editRecord == "1":
    mycursor.execute("SELECT firstname FROM patients WHERE id = %s" % patient_id)
    fetchVal = mycursor.fetchall()
    currentVal = fetchVal[0][0]
    print("\nCurrent first name: ",currentVal)
    newVal = input("\nPlease enter the updated first name: ")
    eventlog.createEditLog(uid,"patients","firstname",patient_id,currentVal,newVal)
    try:
      connectDataDB()
      mycursor.execute("UPDATE patients SET firstname = '%s' WHERE id = %s" % (newVal,patient_id))
      dbconnection.mydb.commit()
      print("Updated successfully.")
      return
    except:
      print("Error updating the record. Please try again.")
      return
    
  elif editRecord == "2":
    mycursor.execute("SELECT lastname FROM patients WHERE id = %s" % patient_id)
    fetchVal = mycursor.fetchall()
    currentVal = fetchVal[0][0]
    print("\nCurrent last name: ",currentVal)
    newVal = input("\nPlease enter the updated last name: ")
    eventlog.createEditLog(uid,"patients","lastname",patient_id,currentVal,newVal)
    try:
      connectDataDB()
      mycursor.execute("UPDATE patients SET lastname = '%s' WHERE id = %s" % (newVal,patient_id))
      dbconnection.mydb.commit()
      print("Updated successfully.")
      return
    except:
      print("Error updating the record. Please try again.")
      return
    
  elif editRecord == "3":
    mycursor.execute("SELECT date_of_birth FROM patients WHERE id = %s" % patient_id)
    fetchVal = mycursor.fetchall()
    currentVal = fetchVal[0][0]
    print("\nCurrent date of birth name: ",currentVal)
    newVal = input("\nPlease enter the updated date of birth (format YYYY-MM-DD): ")
    eventlog.createEditLog(uid,"patients","date_of_birth",patient_id,currentVal,newVal)
    try:
      connectDataDB()
      mycursor.execute("UPDATE patients SET date_of_birth = '%s' WHERE id = %s" % (newVal,patient_id))
      dbconnection.mydb.commit() 
      print("Updated successfully.")
      return
    except:
      print("Error updating the record. Please try again.")
      return
  
#def searchAppointment(attribute, value):
  
#


  
#def editAppointment(attribute, newVal):