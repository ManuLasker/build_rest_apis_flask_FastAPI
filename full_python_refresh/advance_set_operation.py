friends = {"Bob", "Rolf", "Anne"}
abroad = {"Bob", "Anne"}

# set difference operation
local_friends = abroad.difference(friends)
print(local_friends)

# set union operation
total_friends = friends.union(abroad)
print(total_friends)

# intersection
intersection = friends.intersection(abroad)
print(intersection)
