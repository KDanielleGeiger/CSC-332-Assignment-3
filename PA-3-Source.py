import time
import csv
import os.path
from tkinter import *
from functools import partial

##  Toggles spreadsheet generation
##  Used to create Fibonacci_Time.csv
##  *** Enabling this will run BOTH algorithms, regardless of what the user selects ***
generateSpreadsheet = False

##  Creates the UI
def main():
    window = Tk()
    window.title("Fibonacci Series")

    ##  User entry field
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
        entry.config(fg='light grey')

##  Checks that n is a valid value and calls fibRecursive
def display1(entry, valueStr, timeStr):
    try:
        n = int(Entry.get(entry))
        if n >= 0:
            startTime = time.perf_counter()
            value = fibRecursive(n)
            elapsedTime = round(((time.perf_counter() - startTime) * 1000), 6)

            displayResults(value, elapsedTime, valueStr, timeStr)

            ##  If generateSpreadsheet == True, time fibDynamic as well and call generateResults
            if generateSpreadsheet == True:
                startTime2 = time.perf_counter()
                fibDynamic(n)
                elapsedTime2 = round(((time.perf_counter() - startTime2) * 1000), 6)

                generateResults('Fibonacci_Time.csv', n, value, elapsedTime, elapsedTime2)
        else:
            displayResults('Invalid Input', 'Invalid Input', valueStr, timeStr)
    except (ValueError, RecursionError) as e:
        if isinstance(e, ValueError):
            displayResults('Invalid Input', 'Invalid Input', valueStr, timeStr)
        elif isinstance(e, RecursionError):
            displayResults('Cannot compute', 'Cannot compute', valueStr, timeStr)
        else:
            raise

##  Checks that n is a valid value and calls fibDynamic
def display2(entry, valueStr, timeStr):
    try:
        n = int(Entry.get(entry))
        if n >= 0:
            startTime = time.perf_counter()
            value = fibDynamic(n)
            elapsedTime = round(((time.perf_counter() - startTime) * 1000), 6)

            displayResults(value, elapsedTime, valueStr, timeStr)

            ##  If generateSpreadsheet == True, time fibRecursive as well and call generateResults
            if generateSpreadsheet == True:
                startTime2 = time.perf_counter()
                fibRecursive(n)
                elapsedTime2 = round(((time.perf_counter() - startTime2) * 1000), 6)

                generateResults('Fibonacci_Time.csv', n, value, elapsedTime2, elapsedTime)
        else:
            displayResults('Invalid Input', 'Invalid Input', valueStr, timeStr)
    except (ValueError, RecursionError) as e:
        if isinstance(e, ValueError):
            displayResults('Invalid Input', 'Invalid Input', valueStr, timeStr)
        elif isinstance(e, RecursionError):
            displayResults('Cannot compute', 'Cannot compute', valueStr, timeStr)
        else:
            raise

##  Helper function to format results and display them on the UI
def displayResults(value, time, valueStr, timeStr):
    if isinstance(value, str):
        timeSpent = time
    else:
        timeSpent = str(time) + ' ms'

    if not isinstance(value, str):
        if len(str(value)) > 12:
            value = format(value, '.6e')
        
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
def fibDynamic(n):
    a = b = 1
    for x in range(0, n-1):
        temp = a + b
        a = b
        b = temp
    return b

##  When generateSpreadsheet == True, add results to Fibonacci_Time.csv
def generateResults(filename, n, value, timeRecursive, timeDynamic):
    value1 = (2**n) / n
    value1 = format(value1, '.0e')

    value2 = timeRecursive / timeDynamic
    value2 = format(value2, '.0e')

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
