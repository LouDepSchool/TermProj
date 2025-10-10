glob_res = {}#IMPORTANT. Keys MUST map to a list of 2 numbers. have index 0 be the current amount available, and index 1 be the total amount available
glob_even = {} #EVENTS will consist of a key reprenting the event name, and then a list consisting of a start time, end time, and description.
glob_acc = {} #ACCOUNTS. Key = Username, Value = [Password, Type], where type will either be A for admin or S for standard

def validate_str(in_str): #returns true if there is a special character. Returns false if there is not.
    invalid_chars = ["~", "`", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=",
                    "+", "{", "}", "[", "]", ";", ":", "'", '"', "<", ",", ".", ">", "?", "/", "\\", "|", " " ] #list of invalid characters
    for ch in in_str: #iterates through each character in the string checking for invalid characters
        if ch in invalid_chars:
            print("Cannot contain special characters or spaces")
            return True  #if it finds one, returns true, stopping the search early
    return False #otherwise returns false, 
                  
def save_accs(): #function that saves account file. Will ALWAYS override previous one, as always runs on upon program closing
    with open("accountsFile.txt", "w") as outfile:
        for key in glob_acc: #writes to the accountsFile for every present account.
            outfile.write(f"{key}.{glob_acc[key][0]}.{glob_acc[key][1]} \n") #i dont know why this is adding an extra newline after each account but i coded around it. save_ext() uses the same write functions and doesnt have this issue. whatever

def validate_login(): #function to validate login credentials
    hasRan = False
    while True: #loop continues until a return statement breaks it. Only returns on valid login
        if hasRan: #offers users a different way out if they can't login, but only does so after running at least once
            print("Alternatively, type 'New Account' to backout and make a new account.")
        username = input("What is your account username? ").strip()
        if username in glob_acc: #checks to see if the username exists
            password = input("What is your account password? ").strip()
            if password == glob_acc[username][0]: #validates the password
                return username, glob_acc[username][1]
            else:
                print("Invalid Password. Try Again.") #error for bad password
        elif username == "New Account": #out (account creation)
            return make_acc(1)
        else:
            print("Invalid Username. Try Again.") #error for bad username
        hasRan = True

def make_acc_embed(): #an embedded function for general code reuse
    valid_password = False
    valid_user = False
    username = ""
    password = ""
    while not valid_user: #want this to run until a valid username is entered, which is only true IF username does not already exist AND it contains no special characters
        username = input("What's your username? May not contain any special characters or spaces. ").strip()
        if username in glob_acc: #checks keys in accounts to ensure username isnt already present
            print("Cannot share usernames with another user.")
        spec_char = validate_str(username) #validates no special characters
        valid_user = (username not in glob_acc) and (not spec_char)
    while not valid_password:
        password = input("What is your password? No spaces or special characters. ").strip()
        valid_password = validate_str(password)
    return username, password

def make_acc(mode): #function for making account
    if mode == 0: #ONLY applies on first boot/missing account list
        username, password = make_acc_embed() #calls more generalized account creation
        glob_acc.update({username:[password, "A"]}) #First created user will always be an admin
        print("Account creation successful! Welcome new admin.")
        return username, "A" #returns the username and account type
    else: #all other account creation
        username, password = make_acc_embed()
        if(input("If you're a new admin, please enter the admin password now. !!!IMPORTANT!!! You only have one try: ") == "SUPERADMINPASSWORD"):
            #allows the user a SINGLE chance to have an admin level account. Theoretically you'd have this infront of you during account creation...
            glob_acc.update({username: [password, "A"]})
            print("Account creation successful! Welcome new admin.")
            return username, "A"
        else:
            glob_acc.update({username:[password, "S"]}) #makes the user a standard user 
            print("Account creation successful! Welcome standard user")
            return username, "S"
        
def acc_lookup(): #function for finding an account. accountsFile will always be read
    accFile = "accountsFile.txt"
    try:
        test = open(accFile) #looks for the account file
        test.close()
        with open(accFile, "r") as accounts:
            for line in accounts: #fills in the accounts dictionary
                if not line.isspace(): #skip empty line. dunno why it's adding extra empty newlines...
                    username, password, accType = line.split(".")
                    glob_acc.update({username:[password, accType]})
        choice = input("Would you like to login to an existing account, or make a new one? Type 1 for Login, and 2 for New Account. ").strip()
        while choice != "1" and choice != "2": #ensures user ONLY logs in or makes a new account
            choice = input("Invalid input. Try again. ").strip()
        if choice == "1": #user wants to log in to an existing account
            return validate_login()
        else: #user is making a new account
            return make_acc(1)
    except: #the file for loading accounts is missing or corrupted. All other error handling should be     found???
        print(f"{accFile} either missing or corrupted. A new one will be generated. All previous users lost, if any existed. You will become the new Admin.") #obviously a security flaw in reality but let's pretend it's not
        return make_acc(0)

def bootup(): #Allows the user to CHOOSE to load a pre-existing resource.
    name, accType = acc_lookup()
    choice = input("Welcome to the Community Resource Management System! Would you like to load a previously saved file? y/yes/n/no: ").lower().strip()
    while choice[0] != "y" and choice[0] != "n": #choice validation for bootup sequence. 
        print("Invalid option.")
        choice = input("y/yes/n/no only. ").lower().strip()
    if choice[0] == "n": #no, don't load a pre-existing resource document
        add_item(0)
        return 1, name, accType
    else: #yes, load an existing one
        filename = input("What is the file name? Note: file must be in same directory. ").strip()
        if ".txt" not in filename: #append .txt to the end of the filename.
            filename += ".txt"
        try: #attempts to open the filename specified. if it CANNOT do so, it just defaults to standard fresh boot/no load
            test = open(filename)
            test.close() #open and close the file quickly to test if file is present
            with open(filename, "r") as readFile:
                i = 0
                for line in readFile: #when saving a resource preset as "mode.key.currVal.maxVal", so we're going to assume that is the method wewill be reading in
                    if i == 0: #only on the first iteration will the transaction number be present
                        num = int(line)
                        i += 1 #we only care about i for the first line read, so dont bother updating it elsewise
                    else:
                        res = line.split(".")
                        if(res[0] == "0"): #mode "0" represents a resource.
                            glob_res.update({res[1].title():[int(res[2]),int(res[3])]})
                        else: #mode "1" represents an event.
                            glob_even.update({res[1].title():[res[2], res[3], res[4]]})
            print("File loaded successfully!")
            return num, name, accType
        except:
            print("File is either missing or corrupted. Defaulting to standard, non-load boot.")
            add_item(0)
            return 1, name, accType

def num_val_loop(n): #loop to get valid digit.
    num = 0
    hasRun = False
    while num == 0: #digit validation
        if hasRun:
            print("Must be a non-zero positive integer") #error message
        try_num = input(f'How much of/many {n} do you have? ')
        num = validate_digit(try_num)
        hasRun = True
    return num

def validate_digit(r): #validate if is digit, then return them
    if r.isdigit() and int(r) > 0:
        r_avail = int(r)
    else:
        r_avail = 0
    return r_avail

def print_trx(r, qty, trx, mem, mode): #prints a transaction
    if mode == 0: #borrows
        print(f"Borrow Approved. {qty} {r}(s) for {mem}")
    elif mode == 1: #returns
        print(f"Return Approved. {qty} {r}(s) for {mem}")
    else: #event creation
        print(f"Event {r} Created for {mem}. Check events for more details ")
    print(f"Ticket #: {trx} - {len(mem)}")

def add_item(mode): #add items to the resource system
    if mode == 0: #initial resource gathering.
        re_name = ""
        i = 0
        while re_name != "Done":
            re_name = input(f'Name of resource {i+1}? (Type "Done" if finished): ').strip().title()
            if(re_name == "Done"):
                continue #skip this iteration
            num = num_val_loop(re_name)
            glob_res.update({re_name:[num, num]}) #adds new item to the dictionary.
            i+= 1
    else: #alternative mode for adding new resources after intialization. Same as above but without the loop
        re_name = input('Name of new resource? ').strip().title()
        num = num_val_loop(re_name)
        if re_name in glob_res: #"re-adding" a resource to a dictionary will just update/override it. Alerts the user to allow them to reconsider,
            selection = input("Warning! This item already exists, adding it again will override the original, including any borrowed amounts. Continue anyway? Input yes/y/no/n").strip().lower()
            if selection[0] == "n":
                print("Cancelled.")
                return #returns to main without adding anything
        glob_res.update({re_name:[num, num]})
        print("New item added! Check inventory to see it.")

def borrow_item(trx_num, name): #function for borrowing items
    rsel = input("Which resource do you want to borrow? ").strip().title()
    qty_str = input("How much? ").strip()
    if not qty_str.isdigit(): #validate digit
        print("-> Invalid. Must be a positive integer.")
    else:
        qty = int(qty_str)
        if qty <= 0: #must be a positive integer
            print("Must be greater than 0. Try Again.")
        else:
            #determining WITH the dictionary. if not in dictionary, stop
            if rsel in glob_res:
                if qty > glob_res[rsel][0]: #prevents avail resource from going negative
                    print("Exceeds current amount available. Try again.")
                else:
                    glob_res[rsel][0] -= qty
                    print_trx(rsel, qty, trx_num, name, 0)
            else:
                print("Unknown resource. Please only choose a valid resource. Try again")

def return_item(trx_num, name): #function for returning items
    rsel = input("Which Resource would you like to return?: ").strip().title()
    qty_str = input("How much? ").strip()
    if not qty_str.isdigit(): #validates digit
        print("-> Invalid. Must be a positive integer.")
    else:
        qty = int(qty_str)
        if qty <= 0: #ensures positive int
            print("Must be greater than 0")
        else:
            if rsel in glob_res: #ensures that the returned item is in our resources
                if(qty + glob_res[rsel][0] <= glob_res[rsel][1]): #makes sure we're not exceeding our current max
                    glob_res[rsel][0] += qty
                    print_trx(rsel, qty, trx_num, name, 1) 
                else:
                    print("You're returning too much! Try again, make sure you're not giving us some of your stuff...")
            else:
                print("Unknown Resource. Try Again.")

def change_tot():#function for changing totals
    rsel = input("Which Resource are you going to update? ").strip().title()
    new_str = input("New AVAILABLE count (non-negative integer): ").strip()
    if new_str.isdigit():
        new_count = int(new_str)
        if(new_count>0):
            if rsel in glob_res: #validates in resources.
                glob_res[key] = [new_count, new_count] #updates the count to the new counts to be the new totals
                print(f'Resource Updated. {rsel} now has {new_count} available and total.')
            else:
                print("Unknown Resource. Try again")
        else:
            print("Try Again. Must be non-negative integer.")
    else:
        print("Try again. Must be a non-negative integer")

def delete_item():#function for deleting a resource entirely
    rsel = input("Which resource do you want to delete? ").title()
    if rsel in glob_res: #validate selection
        confirm = input(f"Are you ABSOLUTELY SURE you want to remove {rsel} from your community resources? Confirm with y/yes/n/no ").strip().lower()
        if confirm[0] == "y": #Double check to make sure the user actually wants to delete the item!!
            glob_res.pop(rsel)
            print("Resource deleted. Check inventory to confirm.")
        else:
            print("Deletion Cancelled")
    else:
        print("Unknown Resource.")

def add_event(trx_num, userName): #function for adding events
    name = input("What's the name of your event? ").strip().title()
    startTime = input("What's the start time of your event? ").strip()
    endTime = input("What's the ending time of your event? ").strip()
    desc = input("Write a breif description: ")
    print_trx(name, 0, trx_num, userName, 2)
    glob_even.update({name:[startTime, endTime, desc]})

def save_ext(trx_num): #save resources and events as an external file
    filename = input("What would you like to name the file? ").strip()
    if ".txt" not in filename: #automatically append .txt to file if not present.
        filename += ".txt"
    with open(filename, "w") as outfile:
        outfile.write(f"{trx_num} \n") #writes the transaction number as the very first line
        for key in glob_res:
            outfile.write(f"0.{key}.{glob_res[key][0]}.{glob_res[key][1]} \n") #writes all resources as 0.key.CurrentValue.MaxValue
        for key in glob_even:
            outfile.write(f"1.{key}.{glob_even[key][0]}.{glob_even[key][1]}.{glob_even[key][2]} \n") #writes all events as 1.key.StartTime.EndTime.Description
    print(f"File created in current directory as {filename}!")
    
#get resources
trx_num, name, accType = bootup()
choices = "1) View Inventory \n" "2) Borrow \n" "3) Return \n" "4) Edit Available Counts \n" "5) Add Resource \n" "6) Remove Resource \n" "7) Add Event \n" "8) View Events \n" "10) Save Resources And Events As External File \n" "11) Quit \n" #list of choices to make printing easier
choice = ""
while(choice != "11"):
    print("\n---Main Menu---")
    print(choices)
    choice = input("Selection: ").strip()
    choice = str(validate_digit(choice)) #since the while loop requires a string, we use strings for rest of comparisons as well.
    if(choice == "1"): #see inventory
      print("\n---Inventory---")
      for key in glob_res:
          print(f"{key}: {glob_res[key][0]} currently available, with {glob_res[key][1]} max. ")
    elif(choice == "2"): #borrow
        borrow_item(trx_num, name)
        trx_num += 1
    elif(choice == "3"): #return
        return_item(trx_num, name)
        trx_num += 1
    elif(choice == "4"): #change totals
        change_tot()
    elif(choice == "5"): #adding a new resource.
        add_item(1) #just add a new mode for adding resources, like earlier with transaction types
    elif(choice == "6"): #removing an item
        delete_item()
    elif(choice == "7"): #adding an event
        add_event(trx_num, name)
        trx_num += 1
    elif(choice == "8"): #print all events
        for key in glob_even:
            print(f"Event: {key}. Start time: {glob_even[key][0]}. End time: {glob_even[key][1]}. Description: {glob_even[key][2]}")
    elif(choice == "10"): #save current resources as an external file to be loaded at a later date
        save_ext(trx_num)
    elif(choice == "11"): #quit
        print("\nExiting CRMS. Goodbye.")
        save_accs()
    else: #default
        print("Invalid choice.")
 