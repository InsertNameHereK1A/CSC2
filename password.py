import tkinter as tk

def closed():
    root.destroy()

def check_login():
    global AccountDataBase
    AccountDataBase = [['bob','password123'],['john','password']]
    username = username_entry.get()
    password = password_entry.get()
    
    for i in range(0, len(AccountDataBase)):
        if username == AccountDataBase[i][0] and password == AccountDataBase[i][1]:
          error_label.config(text="")
          success_label.config(text="Login successful.")
          return
       
        elif username != AccountDataBase[i][0] or password != AccountDataBase[i][1]:
            success_label.config(text="")
            error_label.config(text="Invalid username or password.")
def main():
    global root
    root = tk.Tk()
    root.title("Login")
    root.attributes('-fullscreen', True)
    global username_entry
    global password_entry
    global error_label
    global success_label

    close = tk.Button(root, text=" X ", command=closed, bg="red",fg="white")
    close.place(x=root.winfo_screenwidth() - 24, y=0)
    
    username_label = tk.Label(root, text="Username:")
    username_label.place(x=root.winfo_screenwidth()/2 - 30, y = root.winfo_screenheight()/2 - 100)
    username_entry = tk.Entry(root)
    username_entry.place(x=root.winfo_screenwidth()/2 - 58, y = root.winfo_screenheight()/2 - 75)

    password_label = tk.Label(root, text="Password:")
    password_label.place(x=root.winfo_screenwidth()/2 - 28, y = root.winfo_screenheight()/2 - 50)
    password_entry = tk.Entry(root, show="*")
    password_entry.place(x=root.winfo_screenwidth()/2 - 58, y = root.winfo_screenheight()/2 - 25)

    login_button = tk.Button(root, text="Login", command=check_login)
    login_button.place(x=root.winfo_screenwidth()/2 - 20, y = root.winfo_screenheight()/2)

    success_label = tk.Label(root, text="", fg="green")
    success_label.place(x=root.winfo_screenwidth()/2 - 50, y = root.winfo_screenheight()/2 + 20)
    error_label = tk.Label(root, text="", fg="red")
    error_label.place(x=root.winfo_screenwidth()/2 - 50, y = root.winfo_screenheight()/2 + 20)

    root.mainloop()

if __name__ == "__main__":
    main()



