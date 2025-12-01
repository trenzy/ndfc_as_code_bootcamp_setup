import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Function to extract the serial number from a Nexus 9K switch
def get_serial_number(switch_ip, username, password):
    """
    Retrieves the serial number of a Nexus 9K switch using NX-API.

    Args:
        switch_ip (str): Management IP address of the switch.
        username (str): Username for authentication.
        password (str): Password for authentication.

    Returns:
        str: Serial number of the switch or an error message.
    """
    # NX-API endpoint URL
    url = f"https://{switch_ip}/ins"

    # Headers for the API request
    headers = {
        "Content-Type": "application/json-rpc"
    }

    # Payload for the "show version" command
    payload=[
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "show inventory chassis",
          "version": 1
        },
        "id": 1
      }
    ]


    try:
        # Send the POST request to the NX-API
        response = requests.post(url, headers=headers, data=json.dumps(payload), auth=(username, password), verify=False)

        # Check if the response status code indicates success
        if response.status_code == 200:
            # Parse the JSON response
            response_json = response.json()

            # Extract the serial number from the response
            try:
                serial_number = response_json["result"]["body"]["TABLE_inv"]["ROW_inv"]["serialnum"]
                return f"{switch_ip}: Serial Number: {serial_number}"
            except KeyError:
                return f"{switch_ip}: Error: Unable to extract the serial number from the response."
        else:
            return f"{switch_ip}: Error: Received status code {response.status_code} from the switch."

    except requests.exceptions.RequestException as e:
        return f"{switch_ip}: Error: Unable to connect to the switch. Exception: {e}"


# Main function
if __name__ == "__main__":
    # List of switches with their management IP addresses
    switches = [
        "198.18.133.201",  
        "198.18.133.202",  
        "198.18.133.203",  
        "198.18.133.204",  
        "198.18.133.205",  
        "198.18.133.206",  
        "198.18.133.207",  
        "198.18.133.208",  
    ]

    # Credentials for all switches
    username = "admin"  # Replace with your username
    password = "C1sco12345"  # Replace with your password

    # Loop through each switch and retrieve its serial number
    print("Retrieving serial numbers for the switches...\n")
    for switch_ip in switches:
        result = get_serial_number(switch_ip, username, password)
        print(result)