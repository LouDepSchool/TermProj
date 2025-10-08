glob_res = {}#IMPORTANT. Keys MUST map to a list of 2 numbers. have index 0 be the current amount available, and index 1 be the total amount available
glob_even = {} #EVENTS will consist of a key reprenting the event name, and then a list consisting of a start time, end time, and description.

def bootup(): #Allows the user to CHOOSE to load a pre-existing resource.
    choice = input("Welcome to the Community Resource Management System! Would you like to load a previously saved file? y/yes/n/no: ").lower().strip()
    while choice[0] != "y" and choice[0] != "n": #choice validation for bootup sequence. 
        print("Invalid option.")
        choice = input("y/yes/n/no only. ").lower().strip()
    if choice[0] == "n": #no, don't load a pre-existing resource document
        add_item(0)
    else: #yes, load an existing one
        filename = input("What is the file name? Note: file must be in same directory. ").strip()
        if ".txt" not in filename: #append .txt to the end of the filename.
            filename += ".txt"
        try: #attempts to open the filename specified. if it CANNOT do so, it just defaults to standard fresh boot/no load
            test = open(filename)
            test.close() #open and close the file quickly to test if file is present
            with open(filename, "r") as readFile:
                for line in readFile: #when saving a resource preset as "mode.key.currVal.maxVal", so we're going to assume that is the method wewill be reading in
                    res = line.split(".")
                    if(res[0] == "0"): #mode "0" represents a resource.
                        glob_res.update({res[1].title():[int(res[2]),int(res[3])]})
                    else: #mode "1" represents an event.
                        glob_even.update({res[1].title():[res[2], res[3], res[4]]})

                    
        except:
            print("File is either missing or corrupted. Deefaulting to standard, non-load boot.")
            add_item(0)

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
    
#get resources
bootup()
trx_num = 1
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
          print(f"{key}: {glob_res[key][0]} currently available, with {glob_res[key][1]} to start. ")
    elif(choice == "2"): #borrow
        member = input("What's your name? ").strip()
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
                        print_trx(rsel, qty, trx_num, member, 0)
                        trx_num+=1
                else:
                    print("Unknown resource. Please only choose a valid resource. Try agaim")
    elif(choice == "3"): #return
        member = input("What's your name? ").strip()
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
                        print_trx(rsel, qty, trx_num, member, 1)
                        trx_num += 1 
                    else:
                        print("You're returning too much! Try again, make sure you're not giving us some of your stuff...")
                else:
                    print("Unknown Resource. Try Again.")
    elif(choice == "4"): #change totals
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
    elif(choice == "5"): #adding a new resource.
        add_item(1) #just add a new mode for adding resources, like earlier with transaction types
    elif(choice == "6"): #removing an item
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
    elif(choice == "7"): #adding an event
        name = input("What's the name of your event? ").strip().title()
        startTime = input("What's the start time of your event? ").strip()
        endTime = input("What's the ending time of your event? ").strip()
        desc = input("Write a breif description: ")
        userName = input("What is your name? ").strip()
        print_trx(name, 0, trx_num, userName, 2)
        glob_even.update({name:[startTime, endTime, desc]})
        trx_num+=1
    elif(choice == "8"): #print all events
        for key in glob_even:
            print(f"Event: {key}. Start time: {glob_even[key][0]}. End time: {glob_even[key][1]}. Description: {glob_even[key][2]}")
    elif(choice == "10"): #save current resources as an external file to be loaded at a later date
        filename = input("What would you like to name the file? ").strip()
        if ".txt" not in filename: #automatically append .txt to file if not present.
            filename += ".txt"
            with open(filename, "w") as outfile:
                for key in glob_res:
                    outfile.write(f"0.{key}.{glob_res[key][0]}.{glob_res[key][1]} \n")
                for key in glob_even:
                    outfile.write(f"1.{key}.{glob_even[key][0]}.{glob_even[key][1]}.{glob_even[key][2]}")
            print(f"File created in current directory as {filename}!")
    elif(choice == "11"): #quit
        print("\nExiting CRMS. Goodbye.")
    else: #default
        print("Invalid choice.")


    