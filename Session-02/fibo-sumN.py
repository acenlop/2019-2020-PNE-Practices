#EXCERCICE 3

def fibon(n):
    if n<0:
        print("Incorrect input")
    # First Fibonacci number is 0
    elif n==1:
        return 0
    # Second Fibonacci number is 1
    elif n==2:
        return 1
    else:
        return fibon(n-1)+fibon(n-2)

def fibosum(n):
    fibonacci = 0
    for i in range(1,n+1):
        fibonacci = fibonacci + fibon(i)
    return fibonacci

n = int(input("Enter a number for the fibonacci series:"))
print("The sum of the first", n, "terms of the Fibonacci series:", fibosum(n))
