
def sumn(n):
    sum = 0
    for i in range(1, n+1):
        sum = sum + i
    return sum

print("Sum of 1-20:", sumn(20))
print("Sum of 1-100:", sumn(100))