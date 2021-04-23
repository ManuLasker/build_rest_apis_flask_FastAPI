print(5 == 5)
print(5 > 5)
print(10 != 10)

# Comparisons: ==, !=, >, <, >=, <=

friends = ["Rolf", "Bob"]
abroad = ["Rolf", "Bob"]

print(friends == abroad)
print(friends is abroad) # two elements are the same exact thing

abroad = friends
print(friends is abroad)
print(friends is ["Rolf", "Bob"])