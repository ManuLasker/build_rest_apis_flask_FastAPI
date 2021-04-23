def divide(dividend, divisor):
    if divisor == 0:
        raise ZeroDivisionError("Divisor cannot be 0")
    return dividend/divisor

grades = [78, 99, 85, 100]
grades = []
try:
    average = divide(sum(grades), len(grades))
except ZeroDivisionError as e:
    print(e)
    print('There are no grades yet in your list')
else: # if all good
    print(average)
finally: # no matther anything
    print("whatever")