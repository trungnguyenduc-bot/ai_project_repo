def giai_thua(n):
    if n < 0:
        return "Invalid input: factorial is not defined for negative numbers."
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

number = int(input("Enter a number: "))
print(f"The factorial of {number} is {giai_thua(number)}")
