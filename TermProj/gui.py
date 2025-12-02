import tkinter as tk
from tkinter import messagebox, simpledialog
import TermProj as crms 

def clear(frame):
    for widget in frame.winfo_children():
        widget.destroy()

#start up screen 

def show_start_menu():
    clear(root)

    title = tk.Label(root, text="Community Resource Management System", font=("Arial", 18))
    title.pack(pady=20)

    load_btn = tk.Button(root, text="Load System / Login", width=30, command=start_system)
    load_btn.pack(pady=10)

    quit_btn = tk.Button(root, text="Quit", width=30, command=root.quit)
    quit_btn.pack(pady=10)


def start_system():
    global username, accType, trx

    clear(root)

    #username, accType = crms.acc_lookup()
    root.iconify()
    trx, username, accType = crms.bootup()
    root.deiconify()
    root.lift()
    messagebox.showinfo("Welcome", f"Logged in as {username}")

    show_user_menu()

#user menu 

def show_user_menu():
    clear(root)

    tk.Label(root, text=f"Welcome, {username}", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="Borrow Resource", width=30, command=gui_borrow).pack(pady=5)
    tk.Button(root, text="Return Resource", width=30, command=gui_return).pack(pady=5)
    tk.Button(root, text="View Resources", width=30, command=gui_view_resources).pack(pady=5)
    tk.Button(root, text="Event Menu", width=30, command=show_event_menu).pack(pady=5)
    tk.Button(root, text="View Summary of Resources", width=30, command=gui_summary).pack(pady=5)
    tk.Button(root, text="Save Externally", width = 30, command=gui_save).pack(pady=5)
    if accType == "A":
        tk.Button(root, text="Admin: Edit Resources", width = 30, command= gui_edit_resource)
        tk.Button(root, text="Admin: Manage Accounts", width=30, command=show_admin_menu).pack(pady=5)
        tk.Button(root, text="Admin: Add New Resource", width=30, command=gui_add_resource).pack(pady=5)

    tk.Button(root, text="Logout", width=30, command=gui_logout).pack(pady=10)
    tk.Button(root, text="Save & Quit", width=30, command=safe_exit).pack(pady=20)

def gui_summary():
    text = "Resources:\n"
    for r in crms.glob_res:
        name, cur, total = r.getValues()
        text += f"  {name}: {cur}/{total}\n"
    text+= "Events:\n"
    for e in crms.glob_even:
        name, s, eT, desc = e.getValues()
        text += f"  {name}:\n    {s} - {eT}\n    {desc}\n\n"
    messagebox.showinfo("Summary", text)
  
def gui_save():
    try:
        root.iconify()
        crms.save_ext(trx)
        root.deiconify()
        root.lift()
        messagebox.showinfo("Done", "Saving success.")
    except:
        messagebox.showerror("Error", "Something went wrong.")

def gui_edit_resource():
    try:
        root.iconify()
        crms.change_tot()
        root.deiconify()
        root.lift()
        messagebox.showinfo("Done", "Totals editted Successfully.")
    except:
        messagebox.showerror("Error", "Something went wrong.")

def gui_logout():
    global username, accType
    try:
        root.iconify()
        username, accType = crms.validate_login()
        root.deiconify()
        root.lift()
        messagebox.showinfo("Done", "Logout process completed.")
        show_user_menu()
        
    except:
        messagebox.showerror("Error", "Something went wrong.")

def gui_borrow():
    try:
        root.iconify()
        crms.borrow_item(trx, username)
        root.deiconify()
        root.lift()
        messagebox.showinfo("Done", "Borrow process completed.")
    except:
        messagebox.showerror("Error", "Something went wrong.")

def gui_return():
    try:
        root.iconify()
        crms.return_item(trx, username)
        root.deiconify()
        root.lift()
        messagebox.showinfo("Done", "Return process completed.")
    except:
        messagebox.showerror("Error", "Something went wrong.")


def gui_view_resources():
    text = ""
    for r in crms.glob_res:
        name, cur, total = r.getValues()
        text += f"{name}: {cur}/{total}\n"

    messagebox.showinfo("Resources", text if text else "No resources found.")

def show_event_menu():
    clear(root)

    tk.Label(root, text="Event Options", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="Create Event", width=30, command=gui_add_event).pack(pady=5)
    tk.Button(root, text="View Events", width=30, command=gui_view_events).pack(pady=5)
    tk.Button(root, text="Back", width=30, command=show_user_menu).pack(pady=20)

def gui_add_event():
    root.iconify()
    crms.add_event(trx, username)
    root.deiconify()
    root.lift()
    messagebox.showinfo("Done", "Event added.")

def gui_view_events():
    out = ""
    for e in crms.glob_even:
        name, s, eT, desc = e.getValues()
        out += f"{name}\n{s} - {eT}\n{desc}\n\n"

    messagebox.showinfo("Events", out if out else "No events found.")


def show_admin_menu():
    clear(root)

    tk.Label(root, text="Admin Options", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="Print Accounts", width=30, command=gui_print_accounts).pack(pady=5)
    tk.Button(root, text="Promote Account", width=30, command=crms.prom_acc).pack(pady=5)
    tk.Button(root, text="Demote Account", width=30, command=lambda: crms.dem_acc(username)).pack(pady=5)
    tk.Button(root, text="Delete Account", width=30, command=lambda: crms.del_acc(username)).pack(pady=5)
    tk.Button(root, text="Back", width=30, command=show_user_menu).pack(pady=20)

def gui_print_accounts():
    accs = "\n".join(crms.glob_acc.keys())
    messagebox.showinfo("Accounts", accs if accs else "No accounts found.")


def gui_add_resource():
    root.iconify()
    crms.add_item(1)
    root.deiconify()
    root.lift()
    messagebox.showinfo("Done", "Resource added successfully.")


def safe_exit():
    crms.save_accs()
    messagebox.showinfo("Saved", "All data saved.")
    root.quit()



root = tk.Tk()
root.title("CRMS GUI")
root.geometry("500x500")

username = ""
accType = ""
trx = None

show_start_menu()
root.mainloop()
