###PART 1###

#1
print("A")
print("B")
print("C")

#2
x = 5

if x > 10:
    print("A")

print("B")

###PART 3###
#9
x = 0

if x:
    print("A")
else:
    print("B")

#10
x = "0"

if x:
    print("A")
else:
    print("B")

#11
x = None

if x:
    print("A")
elif x is None:
    print("B")
else:
    print("C")

#12
x = ""

if x:
    print("A")
elif x == "":
    print("B")
else:
    print("C")
