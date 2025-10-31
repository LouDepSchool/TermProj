glob_acc = {} #ACCOUNTS. Key = Username, Value = [Password, Type], where type will either be A for admin or S for standard
#^^^leaving the PRE-OOP account system because it shows off an interesting use of dictionary and list. If ya'll wanna change it to be an object, be my guest
#I already converted everything dealing with Resources and Events to object/methods. Accounts are effectively mini resources. Do with that what you will
glob_res= []
glob_even = []
class Resource: #resource object

    def __init__(self, name: str, currAvail: int, maxAvail: int):
        self.name = name
        self.maxAvail = maxAvail
        self.currAvail = currAvail

    def borrowItem(self, q: int): #borrow item, with quantity q
        if q > self.currAvail: #if the amount you're trying to borrow is greater than what's available, return False
            return False
        else: #otherwise, take that quantity from what's currently available and return true
            self.currAvail -= q
            return True

    def returnItem(self, q: int): #return items, with quantity q
        if self.currAvail + q > self.maxAvail: #if the quantity you want to return is greater than the max available, prevent it and return false
            return False
        else: #otherwise add it to what's currently avaialble and return true
            self.currAvail += q
            return True

    def getValues(self): #returns name, currAvail, then maxAvail as a touple
        return self.name, self.currAvail, self.maxAvail

    def updateValue(self, newQ: int): #updates the max and currently available resources to be the new max quantity, newQ
        self.maxAvail = newQ
        self.currAvail = newQ
        pass

    def getName(self): #returns just the name
        return self.name

class Event: #event object
    def __init__(self, name: str, sT: str, eT: str, desc: str): #name, start time, end time, description
        self.name = name
        self.sT = sT
        self.eT = eT
        self.desc = desc

    def getValues(self): #returns name, start time, end time, and description 
        return self.name, self.sT, self.eT, self.desc

def print_accs(): #prints all accounts
    for key in glob_acc:
        print(f"Account username: {key}")
        if glob_acc[key][1] == "A": #admin level account
            print("Account Level: Admin")
        else: #standard level account
            print("Account Level: Standard")

def prom_acc(): #promotes a standard account to admin level 
    acc = input("What account are you looking to promote? ").strip()
    if acc in glob_acc: #validates if account exists.
        if glob_acc[acc][1] == "A": #already an admin level account
            print("Error: Account already admin level!")
        else:
            glob_acc[acc][1] = "A" #reassigns account to be admin level
            print("Account level promoted to Admin")
    else:
        print("Error: Account does not exist.")

def dem_acc(n): #demotes an account to standard level
    acc = input("What account are you looking to demote? ").strip()
    if acc in glob_acc: #validates in global accounts dictionary
        if acc != n: #makes sure you aren't trying to demote YOURSELF
            if glob_acc[acc][1] == "S": #already a standard level account
                print("Error: Account level already standard.")
            else:
                glob_acc[acc][1] = "S"
                print("Account level demoted to Standard.")
        else:
            print("Error: Cannot demote yourself.")
    else:
        print("Error: Account does not exist.")

def del_acc(n): #deletes an account
    acc = input("What account are you looking to delete? ").strip()
    if acc in glob_acc: #validates account is in the list of accounts
        if acc != n: #validates account is not your own
            confirm = input("Are you sure you want to delete this account? This cannot be undone. yes/y/no/n ").strip().lower()
            if confirm[0] == "y": #double checks if you want to delete the account
                glob_acc.pop(acc)
                print("Account deleted.")
            else:
                print("Account deletion cancelled.")
        else:
            print("Error: Cannot delete own account. ")
    else:
        print("Error: Account does not exist")

def accMan(name): #admin level account management system
    opts = "1) Print Accounts \n" "2) Promote Account \n" "3) Demote Account \n" "4) Delete Account \n" "5) Quit Account Management System \n" 
    opt = ""
    while opt != "5":
        print("\n---Account Management---")
        print(opts)
        opt = str(validate_digit(input("Selection: ").strip()))
        if opt == "1":
            print_accs()
        elif opt == "2":
            prom_acc()
        elif opt == "3":
            dem_acc(name)
        elif opt == "4":
            del_acc(name)
        elif opt == "5":
            print("Leaving Account Management System.")
        else:
            print("Invalid Choice.")

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
        valid_password = not validate_str(password)
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
                if not line.isspace(): #Potentially obsolete error handling? Leaving it in just incase.
                    username, password, accType = line.split(".")
                    glob_acc.update({username:[password, accType.strip()]}) #.strip() necessary to avoid unnwanted newline characters that were causing issues.
        choice = input("Would you like to login to an existing account, or make a new one? Type 1 for Login, and 2 for New Account. ").strip()
        while choice != "1" and choice != "2": #ensures user ONLY logs in or makes a new account
            choice = input("Invalid input. Try again. ").strip()
        if choice == "1": #user wants to log in to an existing account
            return validate_login()
        else: #user is making a new account
            return make_acc(1)
    except FileNotFoundError: #the file for loading accounts is missing or corrupted. All other error handling should be     found???
        print(f"{accFile} either missing or corrupted. A new one will be generated. All previous users lost, if any existed. You will become the new Admin.") #obviously a security flaw in reality but let's pretend it's not
        return make_acc(0)

def bootup(): #Allows the user to CHOOSE to load a pre-existing resource.
    name, accType = acc_lookup()
    choice = input("Welcome to the Community Resource Management System! Would you like to load a previously saved file? y/yes/n/no: ").lower().strip()
    if len(choice) == 0:
        choice = "k" #forces invalid on empty input
    while choice == None or choice[0] != "y" and choice[0] != "n": #choice validation for bootup sequence. 
        print("Invalid option.")
        choice = input("y/yes/n/no only. ").lower().strip()
        if len(choice) == 0:
            choice = "k" #forces invalid on empty input
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
                            glob_res.append(Resource(res[1].title(), int(res[2].strip()), int(res[3].strip())))
                        else: #mode "1" represents an event.
                            glob_even.append(Event(res[1].title(), res[2], res[3], res[4].strip()))
            print("File loaded successfully!")
            return num, name, accType
        except FileNotFoundError:
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

def verify_item(n): #verifies the existence of an item in the resource list, then returns true/false as well as its index
    i = 0 
    exist = False
    for j in range(len(glob_res)):
        i = j
        if n == glob_res[j].getName(): #runs through the entire list and tries to find the resource
            exist = True
            break
    return i, exist

def add_item(mode): #add items to the resource system
    if mode == 0: #initial resource gathering.
        re_name = ""
        i = 0
        while re_name != "Done":
            re_name = input(f'Name of resource {i+1}? (Type "Done" if finished): ').strip().title()
            if(re_name == "Done"):
                continue #skip this iteration
            num = num_val_loop(re_name)
            i, exists = verify_item(re_name) #we dont really need i but since the index is returned first we have to capture it somehow
            if not exists:
                glob_res.append(Resource(re_name, num, num))
                i+= 1
            else:
                print("Error, already added that resource.")
    else: #alternative mode for adding new resources after intialization. Same as above but without the loop
        re_name = input('Name of new resource? ').strip().title()
        num = num_val_loop(re_name) 
        i, exists = verify_item(re_name)
        if exists: #"re-adding" a resource to a dictionary will just update/override it. Alerts the user to allow them to reconsider,
            selection = input("Warning! This item already exists, adding it again will override the original, including any borrowed amounts. Continue anyway? Input yes/y/no/n ").strip().lower()
            if selection[0] == "n":
                print("Cancelled.")
                return #returns to main without adding anything
        if exists:
            glob_res[i].updateValue(num)
        else:
            glob_res.append(Resource(re_name, num, num))
        print("New item added! Check inventory to see it.")

def borrow_item(trx_num, name): #function for borrowing items
    rsel = input("Which resource do you want to borrow? ").strip().title()
    qty_str = input("How much? ").strip()
    i, itemExist = verify_item(rsel)
    if not qty_str.isdigit(): #validate digit
         print("Invalid. Must be a positive integer.")
    else:
         qty = int(qty_str)
         if qty <= 0: #must be a positive integer
            print("Must be greater than 0. Try Again.")
         else:
            if itemExist:
                didBorrow = glob_res[i].borrowItem(qty)
                if didBorrow:
                    print_trx(rsel, qty, trx_num, name, 0)
                else:
                    print("Exceeds current amount available. Try again.")
            else:
                print("Unknown resource. Please only choose a valid resource. Try again")
   
def return_item(trx_num, name): #function for returning items
    rsel = input("Which resource do you want to return? ").strip().title()
    qty_str = input("How much? ").strip()
    i, itemExist = verify_item(rsel)
    if not qty_str.isdigit(): #validate digit
         print("Invalid. Must be a positive integer.")
    else:
         qty = int(qty_str)
         if qty <= 0: #must be a positive integer
            print("Must be greater than 0. Try Again.")
         else:
            if itemExist:
                didBorrow = glob_res[i].returnItem(qty)
                if didBorrow:
                    print_trx(rsel, qty, trx_num, name, 1)
                else:
                    print("Exceeds max amount. Try again.")
            else:
                print("Unknown resource. Please only choose a valid resource. Try again")

def change_tot():#function for changing totals
    rsel = input("Which Resource are you going to update? ").strip().title()
    new_str = input("New AVAILABLE count (non-negative integer): ").strip()
    i, itemExist = verify_item(rsel)
    if new_str.isdigit():
        new_count = int(new_str)
        if new_count>0:
            if itemExist:
                glob_res[i].updateValue(new_count)
                print("Counts updated successfully.")
            else:
                print("Try again. Unknown item.")
        else:
            print("Try Again. Must be non-negative integer.")
    else:
        print("Try again. Must be a non-negative integer")

def delete_item():#function for deleting a resource entirely
    rsel = input("Which resource do you want to delete? ").title()
    i, itemExist = verify_item(rsel)
    if itemExist: #validate selection
        confirm = input(f"Are you ABSOLUTELY SURE you want to remove {rsel} from your community resources? Confirm with y/yes/n/no ").strip().lower()
        if confirm[0] == "y": #Double check to make sure the user actually wants to delete the item!!
            glob_res.pop(i)
            print("Resource deleted. Check inventory to confirm.")
        else:
            print("Deletion Cancelled")
    else:
        print("Unknown Resource.")

def add_event(trx_num, userName): #function for adding events
    name = input("What's the name of your event? ").strip().title()
    startTime = input("What's the start time of your event? ").strip()
    endTime = input("What's the ending time of your event? ").strip()
    desc = input("Write a breif description: ").strip()
    print_trx(name, 0, trx_num, userName, 2)
    glob_even.append(Event(name, startTime, endTime, desc))

def save_ext(trx_num): #save resources and events as an external file
    filename = input("What would you like to name the file? ").strip()
    if ".txt" not in filename: #automatically append .txt to file if not present.
        filename += ".txt"
    with open(filename, "w") as outfile:
        outfile.write(f"{trx_num} \n") #writes the transaction number as the very first line
        for i in range(len(glob_res)):
            n, c, m = glob_res[i].getValues()
            outfile.write(f"0.{n}.{c}.{m} \n") #writes all resources as 0.key.CurrentValue.MaxValue
        for i in range(len(glob_even)):
            n, sT, eT, d = glob_even[i].getValues()
            outfile.write(f"1.{n}.{sT}.{eT}.{d} \n") #writes all events as 1.key.StartTime.EndTime.Description
    print(f"File created in current directory as {filename}!")

def summary():
    print("Summary of current resources and events: ")
    print("RESOURCES: ")
    for i in range(len(glob_res)):
        n, c, m = glob_res[i].getValues()
        print(f"{n}: {c} currently available, with {m} max")
    print("EVENTS: ")
    for i in range(len(glob_even)):
        n, sT, eT, d = glob_even[i].getValues()
        print(f"\t {n} starts at {sT}, ends at {eT} and has the following description: ")
        print(f"\t\t {d}")
    
#get resources
def main():
    trx_num, name, accType = bootup()
    choices = "1) View Inventory \n" "2) Borrow \n" "3) Return \n" "4) Edit Available Counts \n" "5) Add Resource \n" "6) Remove Resource \n" "7) Add Event \n" "8) View Events \n" "10) Save Resources And Events As External File \n" "11) Summary \n" "12) Quit \n" "13) Log Out & Log Into a Different Account" #list of choices to make printing easier
    choice = ""
    while(choice != "12"):
        print("\n---Main Menu---")
        print(choices)
        if(accType == "A"):
            print("14) Account Management \n") #only shows this option if admin
        choice = input("Selection: ").strip()
        choice = str(validate_digit(choice)) #since the while loop requires a string, we use strings for rest of comparisons as well.
        if(choice == "1"): #see inventory
            print("\n---Inventory---")
            for i in range(len(glob_res)):
                n, c, m = glob_res[i].getValues()
                print(f"{n}: {c} currently available, with {m} max")
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
            if(accType == "A"):
                delete_item()
            else:
                print("Error: Only Admin level accounts have access to this command.")
        elif(choice == "7"): #adding an event
            add_event(trx_num, name)
            trx_num += 1
        elif(choice == "8"): #print all events
            for i in range(len(glob_even)):
                n, sT, eT, d = glob_even[i].getValues()
                print(f"Event: {n}. Start time: {sT}. End time: {eT}. Description: {d}")
        elif(choice == "10"): #save current resources as an external file to be loaded at a later date
            save_ext(trx_num)
        elif choice == "11":
            summary()
        elif(choice == "12"): #quit
            print("\nExiting CRMS. Goodbye.")
            save_accs()
        elif(choice == "13"): #allows account changing
            name, accType = validate_login()
        elif(choice == "14" and accType == "A"): #this option only shows when logged into an admin account, but just incase.
            accMan(name)
        else: #default
            print("Invalid choice.")
 
if __name__ == "__main__":
    main()