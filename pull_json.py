import json
import os
import requests
from tqdm import tqdm

# Path to the JSON file
json_file = "./data/json_list_to_extract.json"

# Directory to save the extracted JSON files
output_dir = "./data/inputJSONs"

# Load the JSON file
with open(json_file, "r") as file:
    json_data = json.load(file)

# save failed extraction json
failed_request = []

# Iterate over the URLs and extract the JSONs
for url in tqdm(json_data["urls"]):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Extract the JSON data
        json_content = response.json()

        # Get the last but one part of the URL
        filename = url.split("/")[-2]
        print(filename)

        # Save the JSON data to a file
        output_file = os.path.join(output_dir, f"{filename}.json")
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(json_content, file, ensure_ascii=False)

        print(f"Successfully extracted JSON from {url} and saved as {output_file}")
    except Exception as e:
        print(f"Error extracting JSON from {url}: {str(e)}")
        failed_request.append(url)