import time
from tkinter import *
from functools import partial

def main():
    window = Tk()
    window.title("Fibonacci Series")

    entry = Entry(window)
    entry.grid(row=0, column=0, padx=(15,5))
    entry.insert(0, 'Enter n ≥ 0')
    entry.bind('<FocusIn>', partial(onFocusIn, entry))
    entry.bind('<FocusOut>', partial(onFocusOut, entry))
    entry.config(fg='light grey')

    Button(window, text='Recursive', command=partial(display1, entry)).grid(row=0,column=1)
    Button(window, text='Dynamic', command=partial(display2, entry)).grid(row=0,column=2,padx=(5,15))
    
    window.mainloop()

def onFocusIn(entry, e):
    if entry.get() == 'Enter n ≥ 0':
        entry.delete(0, END)
        entry.config(fg='black')

def onFocusOut(entry, e):
    if entry.get() == '':
        entry.insert(0, 'Enter n ≥ 0')
        entry.config(fg = 'light grey')

def display1(entry):
    try:
        n = int(Entry.get(entry))
        if n >= 0:
            startTime = time.perf_counter()
            print("Call recursive function")
            elapsedTime = round(((time.perf_counter() - startTime) * 1000), 6)
        else:
            print("Not Good")
    except:
        print("Not Good")

def display2(entry):
    try:
        n = int(Entry.get(entry))
        if n >= 0:
            startTime = time.perf_counter()
            print("Call dynamic function")
            elapsedTime = round(((time.perf_counter() - startTime) * 1000), 6)
        else:
            print("Not Good")
    except:
        print("Not Good")

def fibRecursive(n):
    if n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        return (fibRecursive(n-1) + fibRecursive(n-2))

if __name__ == "__main__":
    main()
