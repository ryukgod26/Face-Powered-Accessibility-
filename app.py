import tkinter as tk

app = tk.Tk()
app.title('Face Powered Accessibility')
app.geometry("500x200")

label = tk.Label(app,text='Testing',font=('Arial',14))
label.pack(pady=20)

def on_click():
    label.config(text="Button Clicked!")

button = tk.Button(app, text="Click Me", command=on_click)
button.pack()

app.mainloop()
