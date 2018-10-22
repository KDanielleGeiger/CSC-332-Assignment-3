import time
import csv
import os.path
from tkinter import *
from functools import partial

##  Toggles whether or not to create/add results to the spreadsheet
##  Used to generate Fibonacci_Time.csv
generateSpreadsheet = True

##  Decorator that caches results for the fibDynamic function
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

##  Creates the UI
def main():
    window = Tk()
    window.title("Fibonacci Series")

    ##  Takes user input
    entry = Entry(window)
    entry.grid(row=0, column=0, padx=(15,5), pady=(15,0))
    entry.insert(0, 'Enter n ≥ 0')
    entry.bind('<FocusIn>', partial(onFocusIn, entry))
    entry.bind('<FocusOut>', partial(onFocusOut, entry))
    entry.config(fg='light grey')

    ##  Displays the result F(n)
    Label(window, text='F(n): ').grid(row=1,column=0,sticky='W',pady=(15,0),padx=(10,0))
    valueStr = StringVar()
    valueStr.set('')
    lbl1 = Label(window, textvariable = valueStr, fg='blue').grid(row=1,column=0,sticky='E',pady=(15,0))

    ##  Displays the result time
    Label(window, text='Time: ').grid(row=2,column=0,sticky='W',padx=(10,0),pady=(0,15))
    timeStr = StringVar()
    timeStr.set('')
    lbl2 = Label(window, textvariable = timeStr, fg='blue').grid(row=2,column=0,sticky='E',pady=(0,15))

    ##  User chooses to use the recursive algorithm or the DP algorithm 
    Button(window, text='Recursive', command=partial(display1, entry, valueStr, timeStr)).grid(row=0,column=1,pady=(15,0))
    Button(window, text='Dynamic', command=partial(display2, entry, valueStr, timeStr)).grid(row=0,column=2,pady=(15,0),padx=(5,15))

    ##  Continue to display UI and wait for user input
    window.mainloop()

##  Removes placeholder text in entry box when user focuses in
def onFocusIn(entry, e):
    if entry.get() == 'Enter n ≥ 0':
        entry.delete(0, END)
        entry.config(fg='black')

##  Replaces placeholder text if user focuses out and no input was given
def onFocusOut(entry, e):
    if entry.get() == '':
        entry.insert(0, 'Enter n ≥ 0')
        entry.config(fg = 'light grey')

##  Checks that n is a valid value and calls fibRecursive
def display1(entry, valueStr, timeStr):
    try:
        n = int(Entry.get(entry))
        if n >= 0:
            startTime = time.perf_counter()
            value = fibRecursive(n)
            elapsedTime = round(((time.perf_counter() - startTime) * 1000), 6)

            displayResults(value, elapsedTime, valueStr, timeStr)

            ##  If generateSpreadsheet == True, time the other algorithm and call generateResults
            if generateSpreadsheet == True:
                startTime2 = time.perf_counter()
                fibDynamic(n)
                elapsedTime2 = round(((time.perf_counter() - startTime2) * 1000), 6)

                generateResults('Fibonacci_Time.csv', n, value, elapsedTime, elapsedTime2)
        else:
            displayResults('Invalid Input', 'Invalid Input', valueStr, timeStr)
    except:
        displayResults('Invalid Input', 'Invalid Input', valueStr, timeStr)

##  Checks that n is a valid value and calls fibDynamic
def display2(entry, valueStr, timeStr):
    try:
        n = int(Entry.get(entry))
        if n >= 0:
            startTime = time.perf_counter()
            value = fibDynamic(n)
            elapsedTime = round(((time.perf_counter() - startTime) * 1000), 6)

            displayResults(value, elapsedTime, valueStr, timeStr)

            ##  If generateSpreadsheet == True, time the other algorithm and call generateResults
            if generateSpreadsheet == True:
                startTime2 = time.perf_counter()
                fibRecursive(n)
                elapsedTime2 = round(((time.perf_counter() - startTime2) * 1000), 6)

                generateResults('Fibonacci_Time.csv', n, value, elapsedTime2, elapsedTime)
        else:
            displayResults('Invalid Input', 'Invalid Input', valueStr, timeStr)
    except:
        displayResults('Invalid Input', 'Invalid Input', valueStr, timeStr)

##  Helper function to format results and display them on the UI
def displayResults(value, time, valueStr, timeStr):
    if isinstance(value, str):
        timeSpent = time
    else:
        timeSpent = str(time) + ' ms'
        
    valueStr.set(value)
    timeStr.set(timeSpent)

##  The recursive Fibonacci algorithm
def fibRecursive(n):
    if n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        return (fibRecursive(n-1) + fibRecursive(n-2))

##  The dynamic Fibonacci algorithm
##  Uses cache decorator to cache results and improve performance
@cache
def fibDynamic(n):
    a = b = 1
    for x in range(0, n-1):
        temp = a + b
        a = b
        b = temp
    return b

def generateResults(filename, n, value, timeRecursive, timeDynamic):
    value1 = (2**n) / n

    value2 = timeRecursive / timeDynamic

    ##  If the file does not exist, create it and add the results to it
    if os.path.isfile(filename) == False:
        with open(filename, mode='w', newline='') as file:
            fieldnames = ['n', 'F(n)', 'T1: Time spent on the recursive algorithm (milliseconds)',
                          'T2: Time spent on the DP algorithm (milliseconds)', 'Value of (2^n)/n', 'Value of T1/T2']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerow({'n': n, 'F(n)': value, 'T1: Time spent on the recursive algorithm (milliseconds)': timeRecursive,
                             'T2: Time spent on the DP algorithm (milliseconds)': timeDynamic,
                             'Value of (2^n)/n': value1, 'Value of T1/T2': value2})
    ##  If the file already exists, append the results to the existing file
    else:
        with open (filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow((n, value, timeRecursive, timeDynamic, value1, value2))

if __name__ == "__main__":
    main()
