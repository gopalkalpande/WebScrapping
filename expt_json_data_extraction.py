import os
import random
import jsonschema, json
from genson import SchemaBuilder
import pandas as pd 

# Path to the input JSONs folder
folder_path = './data/inputJSONs'

# Get a list of all hjson files in the folder
hjson_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]

# Select 50 random hjson files
# random_files = random.sample(hjson_files, 1)

# Iterate over the selected files
for file in hjson_files[0:10000]:
    file_path = os.path.join(folder_path, file)
    
    # Read the JSON data from the file
    with open(file_path, 'r') as f:
        json_data = json.load(f)
    

    # Create a SchemaBuilder
    builder = SchemaBuilder()

    # Define the data variable
    data = json_data

    # Add your data to the builder
    builder.add_object(data)

    # Get the schema
    schema = builder.to_schema()

    # print(schema)
    # # Extract the schema of the JSON data
    # schema = jsonschema.Draft7Validator(json_data).schema
    
    print(schema, '\n--'*20)

    # Extract properties
    properties = schema['properties']

    # Prepare data for DataFrame
    data = {
        'Property': properties.keys(),
        'Type': [prop['type'] for prop in properties.values()]
    }

    # Create DataFrame
    df = pd.DataFrame(data)

    print(df)
    # Convert the schema to CSV format and save it to a file
    # (You'll need to implement this part based on your specific requirements)
    # csv_data = convert_schema_to_csv(schema)
    # save_csv_data(csv_data, file + '.csv')