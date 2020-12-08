import authentication
import operations
import getpass
import eventlog

### Function Definitions ###
def inputUsernameWrapper(newUser:bool) -> str:
  """
  Wrapper to validate user input for username entry.
  Ensures that entered string is following the validation rules and if so returns the entered string.
  
  Differentiates between new user registration or existing login for input prompt text.
  """
  if newUser == True:
    inputUser = input("\nPlease enter your Desired Username: ")
  elif newUser == False:
    inputUser = input("\nPlease enter your Username: ")
  if operations.sanitizeInput(inputUser,"username") == True:
    return inputUser
  else:
    print("Entered username is invalid. Please check and try again.")
    return inputUsernameWrapper(newUser)
  
def inputNameWrapper(nameType:str) -> str:
  """
  Wrapper to validate user input for first and last name entry.
  Ensures that entered string is following the validation rules and if so returns the entered string.
  
  Differentiates between first or last name for input prompt text.
  """
  if nameType == "first":
    inputName = input("\nFirst Name: ")
  elif nameType == "last":
    inputName = input("Last Name: ")
  if operations.sanitizeInput(inputName,"name") == True:
    return inputUser
  else:
    print("Entered %s name is invalid. Please check and try again." % nameType)
    return inputNameWrapper(nameType)

def handleLogin() -> tuple:
  """
  Function to handle user login. Asks for user username and password input.
  If successful, returns authenticated user data as tuple: (user id, username, first name, last name).
  If unsuccesful, displays error (handled by authentication module) and returns user to start of function to input again.
  """
  inputUser = inputUsernameWrapper(newUser=False)
  inputPass = getpass.getpass(prompt="Please enter you Password: ")
  activeUser = authentication.existingUser(inputUser,inputPass)
  if activeUser != None:
    return activeUser
  else:
    return handleLogin()

def handleRegistration() -> tuple:
  """
  Function to handle user registration. Asks for desired username, password, first name and last name to sign up.
  If successful, sends user to handleLogin function to login with created credentials and returns authenticated tuple.
  If unsuccesful, displays error (handled by authentication module) and returns user to start of function.
  """
  inputUser = inputUsernameWrapper(newUser=True)
  inputPass = getpass.getpass(prompt="Desired Password: ")
  confirmPass = getpass.getpass(prompt="Confirm Password: ")  
  if inputPass == confirmPass:
    inputFirstName = inputNameWrapper("first")
    inputLastName = inputNameWrapper("last")   
    signupStatus = authentication.newUser(inputUser,inputPass,inputFirstName,inputLastName) #returns True if successful
    if signupStatus == True:
      return handleLogin()
    else:
      handleRegistration()
  else:
    handleRegistration()
    
def showBanner():
  """
  Draws banner from banner.bin file for motd and first instructions. Used instead of print statements to save space.
  """
  fBanner = open("config/banner.bin", "r")
  banner = fBanner.readlines()
  fBanner.close()
  for line in banner:
    print(line, end='')   

def showOperations():
  """
  Displays main menu operations (search patient, search appointment, log out) and asks for user selection.
  User selection is then referred to inputChoiceWrapper to confirm validity of input.
  If selection is valid, calls handleOperation function with selected option.
  """
  print("\n Please select what you want to do:")
  print(" 1.) Search for a patient")
  print(" 2.) Search for an appointment")
  print(" 3.) Log out")
  userSelect = operations.inputChoiceWrapper(3)
  handleOperations(userSelect)
  
def handleOperations(choice:str):
  """
  This function serves as handler for the selected options in showOperations().
  Depending on the choice, the user is referred to the appropriate function.
  """
  if choice == "1":
    handlePatientSearch()
  elif choice == "2":
    handleAppointmentSearch()
  elif choice == "3":
    print("See you soon!\n")
    exit()
    
def handlePatientSearch():
  """
  Displays patient search options to user and handles user's choice.
  If valid choice and search term are entered, refers to operations module to execute search operation. 
  """
  print("\n Please select how you want to search for the patient:")
  print(" 1.) Search by first name")
  print(" 2.) Search by last name")
  print(" 3.) Search by date of birth")
  print(" 4.) Return to main menu")
  userSelect = operations.inputChoiceWrapper(4)
  
  if userSelect == "1" or userSelect == "2":
      searchTerm = input("\nPlease enter search term: ")
      if operations.sanitizeInput(searchTerm,"name") == True: # checks validity of entered name
        if userSelect == "1":
          operations.searchPatient("firstname",searchTerm,activeUser[0])
        elif userSelect == "2":
          operations.searchPatient("lastname",searchTerm,activeUser[0])
      else:
        print("Invalid name entered. Please check your search term and try again.")
        handlePatientSearch()
    
  elif userSelect == "3":
    searchTerm = input("\nPlease enter date of birth (format YYYY-MM-DD): ")
    if operations.sanitizeInput(searchTerm,"datetime") == True: # checks validity of entered date
      operations.searchPatient("date_of_birth",searchTerm,activeUser[0])
      
    else:
      print("Invalid date of birth entered. Please check your search term and try again.")
      handlePatientSearch()
      
  else:
    showOperations()
    
def handleAppointmentSearch():
  """
  Displays appointment search options to user and handles user's choice.
  If valid choice and search term are entered, refers to operations module to execute search operation. 
  """
  print("\n Please select how you want to search for the appointment:")
  print(" 1.) Search by date")
  print(" 2.) Search by patient ID")
  print(" 3.) Search by consulting staff ID")
  print(" 4.) Return to main menu")
  userSelect = operations.inputChoiceWrapper(4)
  
  if userSelect == "1": # if choice is search by date
    searchTerm = input("\nPlease enter date (format YYYY-MM-DD): ")
    if operations.sanitizeInput(searchTerm,"datetime") == True: # checks validity of entered date
      operations.searchAppointment("date",searchTerm,activeUser[0])
    else:
      print("Invalid date entered. Please check your search term and try again.")
      handleAppointmentSearch()
      
  if userSelect == "2": # if choice is search by patient id
    searchTerm = input("\nPlease enter patient's ID: ")
    try:
      intSearch = int(searchTerm) # tries to convert entered string to integer for id search
      operations.searchAppointment("patient_id",intSearch,activeUser[0])
    except:
      print("Invalid ID entered. Please check your search term and try again.")
      handleAppointmentSearch()
  
  if userSelect == "3": # if choice is search by consulting staff id
    searchTerm = input("\nPlease enter consulting staff's ID: ")
    try:
      intSearch = int(searchTerm) # tries to convert entered string to integer for id search
      operations.searchAppointment("consulting_staff",intSearch,activeUser[0])
    except:
      print("Invalid ID entered. Please check your search term and try again.")
      handleAppointmentSearch()  
      
  else:
    showOperations()

### Start of interface code and main loop ###
showBanner()

userSelect = operations.inputChoiceWrapper(2)
if userSelect == "1":
  activeUser = handleLogin() # Saving the active user credentials in variable to recall for later use
elif userSelect == "2":
  print("\nWelcome to the Queens Medical ASMIS system. Please input the following information to complete your registration.")
  activeUser = handleRegistration()  

while True:
  showOperations()