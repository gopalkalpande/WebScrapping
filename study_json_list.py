import json

# Read the JSON file
with open("./data/json_list_to_extract.json") as file:
    data = json.load(file)

print("count of URLs: ", len(data['urls']))
# Print the keys
for key in data.keys():
    print(key)

