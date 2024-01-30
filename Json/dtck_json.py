import requests
import json

#Variables definition
workspace = "WORKSPACE_ID" #Insert here the datacake Workspace ID
authtoken = "API_TOKEN" #Insert here the generated api token
timerangestart = "2024-01-25T00:00" #Specify here starting time of the desired timespan formatted as YYYY-MM-DDThh:mm
timerangeend = "2024-01-26T00:00" #Specify here the end time of the desired timespan formatted as YYYY-MM-DDThh:mm
resolution = "5m" #Specify here the resolution at which data will be aggregated - use "raw" for no aggregation 
url = 'https://api.datacake.co/graphql/' # API endpoint
file_path = 'test.json' # Path to the output file


# GraphQL query
params = {
    'query': 'query{allDevices(inWorkspace: "'+ workspace +'") {verboseName, id, location, history(timerangestart: "'+ timerangestart +'", timerangeend: "'+ timerangeend +'",resolution: "'+ resolution +'")}}'
}

# Headers for the POST request
headers = {
    'Authorization': 'Token ' + authtoken,
    'Content-Type': 'application/json'
}

# Make the POST request
response = requests.post(url, json=params, headers=headers)

# Convert the response to JSON
if response.status_code == 200:
        # Request was successful, processing the response, converting into JSON
        data = response.json()
else:
    # Request failed, writing to console error code
    print("Error:", response.status_code)
    print(response.text)
    exit()

#Clear file content before appending data to it
open(file_path, 'w').close()

#Initiating the output list
out = []

#Prettifying the output into a nice-formatted JSON
for device in data['data']['allDevices']:
    history_string =  device['history']
    history_data = json.loads(history_string)
    formatted_data = {
            "verboseName": device['verboseName'],
            "id": device['id'],
            "location": device['location'],
            "history": history_data
            }
    out.append(formatted_data)
    
#Writing the list to the desired file converting it into a JSON    
with open(file_path, 'a') as file:
    json.dump(out, file, indent=2)


file_path = 'test.json'  # Replace with your desired file path

# Save the result to a file


print(f"Data saved to {file_path}")