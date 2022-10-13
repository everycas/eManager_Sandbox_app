from mongoman_res import Mongoman
from ini_res import Ini
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox


INI = Ini()
INI.ini_name = 'eMan.ini'
INI.log_name = 'eMan.log'

MONGO = Mongoman()
DB = INI.get(section='main', param='db')

if not DB:
    new_db = MONGO.gen_dbname()
    INI.set(section='main', param='db', data=new_db)

# GUI --------------

root = Tk()
root.title("eManager - 0.2")
root.config(padx=5, pady=5)
root.minsize(width=800, height=600)

# Menu
main = Menu(root)
root.config(menu=main)

# File
file = Menu(main, tearoff=0)
file.add_command(label="Server connect", command='')
file.add_command(label="Db connect", command='')
file.add_separator()
file.add_command(label="Exit", command=root.destroy)

#


main.add_cascade(label="File", menu=file)

root.mainloop()








