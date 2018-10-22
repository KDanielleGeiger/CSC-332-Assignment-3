import time
from tkinter import *
from functools import partial

def cache(fn):
    CACHE = {}

    def wrapper(*args):
        if args in CACHE:
            return CACHE[args]
        else:
            result = fn(*args)
            CACHE[args] = result
            return result

    return wrapper

def main():
    window = Tk()
    window.title("Fibonacci Series")

    entry = Entry(window)
    entry.grid(row=0, column=0, padx=(15,5), pady=(15,0))
    entry.insert(0, 'Enter n ≥ 0')
    entry.bind('<FocusIn>', partial(onFocusIn, entry))
    entry.bind('<FocusOut>', partial(onFocusOut, entry))
    entry.config(fg='light grey')

    Label(window, text='F(n): ').grid(row=1,column=0,sticky='W',pady=(15,0),padx=(10,0))
    valueStr = StringVar()
    valueStr.set('')
    lbl1 = Label(window, textvariable = valueStr, fg='blue').grid(row=1,column=0,sticky='E',pady=(15,0))
    
    Label(window, text='Time: ').grid(row=2,column=0,sticky='W',padx=(10,0),pady=(0,15))
    timeStr = StringVar()
    timeStr.set('')
    lbl2 = Label(window, textvariable = timeStr, fg='blue').grid(row=2,column=0,sticky='E',pady=(0,15))

    Button(window, text='Recursive', command=partial(display1, entry, valueStr, timeStr)).grid(row=0,column=1,pady=(15,0))
    Button(window, text='Dynamic', command=partial(display2, entry, valueStr, timeStr)).grid(row=0,column=2,pady=(15,0),padx=(5,15))
    
    window.mainloop()

def onFocusIn(entry, e):
    if entry.get() == 'Enter n ≥ 0':
        entry.delete(0, END)
        entry.config(fg='black')

def onFocusOut(entry, e):
    if entry.get() == '':
        entry.insert(0, 'Enter n ≥ 0')
        entry.config(fg = 'light grey')

def display1(entry, valueStr, timeStr):
    try:
        n = int(Entry.get(entry))
        if n >= 0:
            startTime = time.perf_counter()
            value = fibRecursive(n)
            elapsedTime = round(((time.perf_counter() - startTime) * 1000), 6)

            displayResults(value, elapsedTime, valueStr, timeStr)
        else:
            displayResults('Invalid Input', 'Invalid Input', valueStr, timeStr)
    except:
        displayResults('Invalid Input', 'Invalid Input', valueStr, timeStr)

def display2(entry, valueStr, timeStr):
    try:
        n = int(Entry.get(entry))
        if n >= 0:
            startTime = time.perf_counter()
            value = fibDynamic(n)
            elapsedTime = round(((time.perf_counter() - startTime) * 1000), 6)

            displayResults(value, elapsedTime, valueStr, timeStr)
        else:
            displayResults('Invalid Input', 'Invalid Input', valueStr, timeStr)
    except:
        displayResults('Invalid Input', 'Invalid Input', valueStr, timeStr)

def displayResults(value, time, valueStr, timeStr):
    if isinstance(value, str):
        timeSpent = time
    else:
        timeSpent = str(time) + ' ms'
        
    valueStr.set(value)
    timeStr.set(timeSpent)

def fibRecursive(n):
    if n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        return (fibRecursive(n-1) + fibRecursive(n-2))

def fibDynamic(n):
    a = b = 1
    if n == 0:
        return 1
    else:
        for x in range(0, n-1):
            temp = a + b
            a = b
            b = temp
    return b

fibDynamic = cache(fibDynamic)

if __name__ == "__main__":
    main()
