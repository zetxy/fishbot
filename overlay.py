import tkinter as tk

root = tk.Tk()
root.title('Tkinter Window Demo')
root.geometry('600x400+50+50')
root.resizable(False, False)
root.attributes('-alpha', 0.1)
root.attributes('-topmost', True)

label = tk.Label(root, text="Hello World! ", font=('Helvetica bold', 15))
label.pack()

root.mainloop()
