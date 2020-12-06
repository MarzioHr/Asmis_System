import authentication
import operations
import getpass
import eventlog

def handleLogin():
  """
  Function to handle user login. Asks for user username and password input.
  If successful, returns authenticated user data as tuple: (user id, username, first name, last name).
  If unsuccesful, displays error (handled by authentication module) and returns user to start of function to input again.
  """
  inputUser = input("\nPlease enter your Username: ")
  inputPass = getpass.getpass(prompt="Please enter you Password: ")
  activeUser = authentication.existingUser(inputUser,inputPass)
  if activeUser != None:
    return activeUser
  else:
    return handleLogin()

def handleRegistration():
  """
  Function to handle user registration. Asks for desired username, password, first name and last name to sign up.Function
  If successful, sends user to handleLogin function to login with created credentials.
  If unsuccesful, displays error (handled by authentication module) and returns user to start of function.
  """
  inputUser = input("\nDesired Username: ") 
  inputPass = getpass.getpass(prompt="Desired Password: ")
  confirmPass = getpass.getpass(prompt="Confirm Password: ")  
  if inputPass == confirmPass:
    inputFirstName = input("\nFirst Name: ")
    inputLastName = input("Last Name: ")    
    signupStatus = authentication.newUser(inputUser,inputPass,inputFirstName,inputLastName) #returns True if successful
    if signupStatus == True:
      handleLogin()
    else:
      handleRegistration()
  else:
    handleRegistration()
    
def showBanner():
  """
  Draws banner from banner.bin file for motd and first instructions. Used instead of print statements to save space.
  """
  fBanner = open("banner.bin", "r")
  banner = fBanner.readlines()
  fBanner.close()
  for line in banner:
    print(line, end='')   

def showOperations():
  """
  Displays main menu operations (search patient, search appointment, log out) and asks for user selection.
  If selection is valid, calls handleOperation function with selected option.
  If selection is invalid, prints error and returns user to start of function. 
  """
  print("\n Please select what you want to do:")
  print(" 1.) Search for a patient")
  print(" 2.) Search for an appointment")
  print(" 3.) Log out")  
  while True:
    userSelect = input("\nSelect option: ")
    if userSelect == "1" or userSelect == "2" or userSelect == "3":
      handleOperations(userSelect)
    else:
      print("Invalid selection. Please check your input and try again.")
  
def handleOperations(choice):
  """
  This function serves as handler for selected 
  """
  if choice == "1":
    handlePatientSearch()
  elif choice == "2":
    handleAppointmentSearch()
  elif choice == "3":
    print("See you soon!\n")
    exit()
    
def handlePatientSearch():
  print("\n Please select how you want to search for the patient:")
  print(" 1.) Search by first name")
  print(" 2.) Search by last name")
  print(" 3.) Search by date of birth")
  print(" 4.) Return to main menu")
  while True:
    userSelect = input("\nSelect option: ")
    if userSelect == "1" or userSelect == "2":
      searchTerm = input("\nPlease enter search term: ")
      if userSelect == "1":
        operations.searchPatient("firstname",searchTerm,activeUser[0])
      elif userSelect == "2":
        operations.searchPatient("lastname",searchTerm,activeUser[0])
    elif userSelect == "3":
      searchTerm = input("\nPlease enter date of birth (format YYYY-MM-DD): ")
      operations.searchPatient("date_of_birth",searchTerm,activeUser[0])  
    elif userSelect == "4":
      showOperations()
    else:
      print("Invalid selection. Please check your input and try again.")
    showOperations()
    
def handleAppointmentSearch():
  print("\n Please select how you want to search for the appointment:")
  print(" 1.) Search by date")
  print(" 2.) Search by time")
  print(" 3.) Search by patient ID")
  print(" 4.) Return to main menu")
  while True:
    userSelect = input("\nSelect option: ")
    if userSelect == "1":
      searchTerm = input("\nPlease enter date (format YYYY-MM-DD): ")
      operations.searchAppointment("date",searchTerm,activeUser[0])
      
    elif userSelect == "2":
      searchTerm = input("\nPlease enter date (format YYYY-MM-DD): ")
      operations.searchAppointment("time",searchTerm,activeUser[0])
      
    elif userSelect == "3":
      searchTerm = input("\nPlease enter patient ID: ")
      operations.searchPatient("patient_id",searchTerm,activeUser[0])  
    elif userSelect == "4":
      showOperations()
    else:
      print("Invalid selection. Please check your input and try again.")
    showOperations()
# start of interface code

showBanner()

while True:
  userSelect = input("Select option: ")
  if userSelect == "1":
    activeUser = handleLogin() # Saving the active user credentials in variable to recall for later use
    break
  elif userSelect == "2":
    print("\nWelcome to the Queens Medical ASMIS system. Please input the following information to complete your registration.")
    handleRegistration()
    break
  else:
    print("Invalid selection. Please check your input and try again.\n")

print("Active user is: ", activeUser)    
    
showOperations()

