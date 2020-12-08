import eventlog
import dbconnection

# set DB cursor
mycursor = dbconnection.mydb.cursor()

def connectDataDB():
  """
  Function to connect to the 'data' database.
  """
  try:
    mycursor.execute("USE data")
  except:
    print("MySQL connection failed.")
  
def sanitizeInput(userInput:str, inputType:str) -> bool: 
  """
  Takes the user input and the type of input as arguments and determines if the input is valid.
  
  username: may include alpha numerical values and special characters '.', '_' and '-'
  name: may include alphabetical values, spaces and special character '-'
  datetime: may include numerical values and special characters '-' and ':'
  password may include alpha numerical values and special characters but will be hashed so no sanatization required.
  """
  validUserSpecial = ('.','_','-')
  validNameSpecial = (' ','-')
  validDateTimeSpecial = (':','-')
  
  if inputType == "username":
    for a in userInput:
      if a.isalnum():
        continue
      elif a in validUserSpecial:
        continue
      else:
        return False
  elif inputType == "name":
    for a in userInput:
      if a.isalpha():
        continue
      elif a in validNameSpecial:
        continue
      else:
        return False
  elif inputType == "datetime":
    for a in userInput:
      if a.isnumeric():
        continue
      elif a in validDateTimeSpecial:
        continue
      else:
        return False
  return True

def inputChoiceWrapper(nChoices:int) -> str:
  """
  Wrapper to validate user input for listed choices.
  nChoices determines the number of choices the user can choose between.nChoices
  
  If choice is valid, the input is returned.
  If invalid, the user is prompted to input again
  """
  userSelect = input("\nSelect option: ")
  try:
    intSelect = int(userSelect)
  except:
    print("Invalid selection. Please check your input and try again.")
    return inputChoiceWrapper(nChoices)
  if intSelect > 0 and intSelect <= nChoices:
    return userSelect
  else:
    print("Invalid selection. Please check your input and try again.")
    return inputChoiceWrapper(nChoices)      
    
def displayResults(result:list, resultType:str, uid:int):
  """
  Function to handle display of found results for search query.
  resultType denotes whether the results are for an appointment or a patient search.
  """
  resultCount = len(result) # counts total number of results
  if resultCount == 0:
    print("No results found, please try again.")
    return
  elif resultCount > 0:
    print("Found a total of %s result(s):" % resultCount)
    print("----------------------------------------------------------------------------------------")
    if resultType == "patient":
      for i in range(0,resultCount):
        print("ID: %s\t Name: %s %s\t Date of Birth: %s\t Consultant ID: %s" % (result[i][0], result[i][1], result[i][2], result[i][3], result[i][4]))
        displayEditChoices("patient", uid)
    if resultType == "appointment":
      for i in range(0,resultCount):
        print("ID: %s\t Date: %s \t Time: %s\t Patient ID: %s\t Consultant ID: %s" % (result[i][0], result[i][1], result[i][2], result[i][3], result[i][4]))
        displayEditChoices("appointment", uid)
    
def displayEditChoices(choiceType:str, uid:int):
  """
  Function to handle choices for edit patient and edit appointment inputs.
  Is called after results are displayed and displays different options for either patients or appointments.
  Asks user to choose whether a record should be edited or not. If yes, asks for the attribute and the record id to be changed.
  
  Once user input is validated, refers to the appropriate edit function call (either 'editPatient' or 'editAppointment') 
  and passes the record id, the user id, and the attribute to be changed as arguments.
  """
  if choiceType == "patient":
    print("\n Please choose an option:")
    print(" 1.) Edit patient record")
    print(" 2.) Return to main menu")
    userSelect = inputChoiceWrapper(2)   
    if userSelect == "1": # user selects to edit a patient's record
      patientID = input("\nPlease enter the ID of the patient you want to edit: ") # input for record id to edit
      try:
        patientID = int(patientID) # attempt to convert string to integer
      except:
        print("Invalid selection. Please check your input and try again.")
        displayEditChoices(choiceType,uid)      
      print("\n What attribute do you want to edit?") # input for attribute to change
      print(" 1.) Patient's first name")
      print(" 2.) Patient's last name")
      print(" 3.) Patient's date of birth")
      print(" 4.) Cancel")
      userSelect = inputChoiceWrapper(4)
      patientChoiceDict = {'1':'firstname','2':'lastname','3':'date_of_birth'} # dict to map input to attributes
      if userSelect == '4': # user selects to cancel
        return
      else:
        editPatient(patientID,uid,patientChoiceDict[userSelect])
    else: # user selects to return to main menu
      return
    
  elif choiceType == "appointment":
    print("\n Please choose an option:")
    print(" 1.) Edit appointment record")
    print(" 2.) Return to main menu")
    userSelect = inputChoiceWrapper(2)   
    if userSelect == "1": # user selects to edit an appointment record
      appointmentID = input("\nPlease enter the ID of the appointment you want to edit: ") # input for record id to edit
      try:
        appointmentID = int(appointmentID) # attempt to convert string to integer
      except:
        print("Invalid selection. Please check your input and try again.")
        displayEditChoices(choiceType,uid)         
      print("\n What attribute do you want to edit?")
      print(" 1.) Appointment date")
      print(" 2.) Appointment time")
      print(" 3.) Consulting Staff ID")
      print(" 4.) Cancel")
      userSelect = inputChoiceWrapper(4)
      appointmentChoiceDict = {'1':'date','2':'time','3':'consulting_staff'} # dict to map input to attributes
      if userSelect == '4': # user selects to cancel
        return
      else:
        editAppointment(appointmentID,uid,ppointmentChoiceDict[userSelect])
    else:
      return
  
def searchPatient(attribute:str, value:str, uid:int):
  """
  Function to handel the actual patient search query.
  Takes as input the search attribute, the search term (value) and the user id that conducts the search.  
  Prior to conducting the search, the function calls the createSearchLog operation to create an event log of the search.
  
  If the search is successful, passes the result list to the displayResults function.
  """
  eventlog.createSearchLog(uid,"patients",attribute,value)
  connectDataDB()
  sql = "Select * FROM patients WHERE " + attribute + " = %(val)s"
  val = {'val':value}
  mycursor.execute(sql,val)
  result = mycursor.fetchall()
  displayResults(result, "patient", uid)
  
def searchAppointment(attribute, value, uid):
  """
  Function to handel the actual appointment search query.
  Takes as input the search attribute, the search term (value) and the user id that conducts the search.  
  Prior to conducting the search, the function calls the createSearchLog operation to create an event log of the search.
  
  If the search is successful, passes the result list to the displayResults function.
  """
  eventlog.createSearchLog(uid,"appointments",attribute,value)
  connectDataDB()
  mycursor.execute("Select * FROM appointments WHERE %(key)s = %(value)s", {'key':attribute, 'value':value})
  result = mycursor.fetchall()
  displayResults(result, "appointment", uid)

def editPatient(patientID:int,uid:int,attribute:str):
  """
  Function to handel the an edit patient operation. Takes as input the patient record id 
  to be edited, the user id that conducts the edit, as well as the attribute to be changed.  
  
  Function asks for user input for the new value of the attribute. Once give, the input is validated
  and then executed as a db update query.
  
  Once the change has gone through successfully, the createEditLog function is called to create an event log
  of what has changed, when it has changed, on what record and by what user.
  """  
  connectDataDB()
  mycursor.execute("SELECT * FROM patients WHERE id = %(id)s", {'id':patientID})
  fetchValues = mycursor.fetchall()
  patientDatabaseDict = {'id':0,'firstname':1,'lastname':2,'date_of_birth':3}
  patientDisplayDict = {'id':'id','firstname':'first name','lastname':'last name','date_of_birth':'date of birth'}
  currentValue = fetchValues[0][patientDatabaseDict[attribute]]
  print("\nCurrent %s: %s" % (patientDisplayDict[attribute], currentValue))
  newValue = input("\nPlease enter the new %s: " % attribute)
  
  if attribute == 'firstname' or attribute == 'lastname':
    if sanitizeInput(newValue, 'name') == False:
      print("Invalid input. Please check your entry and try again.")
      return displayEditChoices('patient',uid)
  elif attribute == 'date_of_birth':
    if sanitizeInput(newValue, 'datetime') == False:
      print("Invalid input. Please check your entry and try again.")
      return displayEditChoices('patient',uid)
   
  try:
    connectDataDB()
    sql = "UPDATE patients SET " + attribute + " = %(value)s WHERE id = %(id)s"
    val = {'value':newValue,'id':patientID}
    mycursor.execute(sql,val)
    dbconnection.mydb.commit()
    eventlog.createEditLog(uid,"patients",attribute,patientID,currentValue,newValue) # create log of edit event in log database
    print("Updated successfully.")
    return
  except:
    print("Error updating the record. Please try again.")
    return displayEditChoices('patient',uid)
      
def editAppointment(appointmentID:int,uid:int,attribute:str):
  """
  Function to handel the edit appointment operation. Takes as input the appointment record id 
  to be edited, the user id that conducts the edit, as well as the attribute to be changed.  
  
  Function asks for user input for the new value of the attribute. Once give, the input is validated
  and then executed as a db update query.
  
  Once the change has gone through successfully, the createEditLog function is called to create an event log
  of what has changed, when it has changed, on what record and by what user.
  """
  connectDataDB()
  mycursor.execute("SELECT * FROM appointments WHERE id = %s", (patientID))
  fetchValues = mycursor.fetchall()
  appointmentDatabaseDict = {'id':0,'date':1,'time':2,'consulting_staff':4}
  appointmentDisplayDict = {'id':'id','date':'date','time':'time','consulting_staff':'consulting staff id'}
  currentValue = fetchValues[0][appointmentDatabaseDict[attribute]]
  print("\nCurrent %s: %s" % (appointmentDisplayDict[attribute], currentValue))
  newValue = input("\nPlease enter the new %s: " % attribute)
  
  if attribute == 'date' or attribute == 'time':
    if sanitizeInput(newValue, 'datetime') == False:
      print("Invalid input. Please check your entry and try again.")
      return displayEditChoices('appointment',uid)
  elif attribute == 'consulting_staff':
    try:
      intCheck = int(newValue)
    except:
      print("Invalid input. Please check your entry and try again.")
      return displayEditChoices('patient',uid)
   
  try:
    connectDataDB()
    sql = "UPDATE patients SET " + attribute + " = %(value)s WHERE id = %(id)s"
    val = {'value':newValue,'id':appointmentID}
    mycursor.execute(sql,val)
    dbconnection.mydb.commit()
    eventlog.createEditLog(uid,"appointments",attribute,appointmentID,currentValue,newValue) # create log of edit event in log database
    print("Updated successfully.")
    return
  except:
    print("Error updating the record. Please try again.")
    return displayEditChoices('appointments',uid)