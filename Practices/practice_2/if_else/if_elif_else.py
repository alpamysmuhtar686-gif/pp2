# ex 1: basic elif
a = 67
b = 67
if a > b:
    print(f"{a} > {b}")
elif a == b:
    print("They're equal")

# ex 2: Multiple elif statements
score = 92

if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
elif score >= 60:
    print("Grade: D")


# ex 3: if the condition returns true, then the other elif's will be ignored
age = 25

if age < 13:
  print("You are a child")
elif age < 20:
  print("You are a teenager")
elif age < 65: # returns "You are an adult" and stops here
  print("You are an adult")
elif age >= 65:
  print("You are a senior")

# ex 4: use elif if there is mutual exclusive cases
day = 3

if day == 1:
  print("Monday")
elif day == 2:
  print("Tuesday")
elif day == 3:
  print("Wednesday")
elif day == 4:
  print("Thursday")
elif day == 5:
  print("Friday")
elif day == 6:
  print("Saturday")
elif day == 7:
  print("Sunday")