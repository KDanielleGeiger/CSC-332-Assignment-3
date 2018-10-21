from tkinter import *

def main():
    window = Tk()
    window.title("Fibonacci Series")
    
    window.mainloop()

def fibRecursive(n):
    if n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        return (fibRecursive(n-1) + fibRecursive(n-2))

if __name__ == "__main__":
    main()
