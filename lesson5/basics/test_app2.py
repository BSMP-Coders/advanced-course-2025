from app2 import send_echo_request


#def send_echo_request(message):
#    url = "http://localhost:5000/echo"
#    data = {"message": message}
    
#    response = requests.post(url, json=data)
    
#    if response.status_code == 200:
#        return f"Server responded: {response.json()['response']}"
#    else:
#        return f"Error: Status code {response.status_code}"

# Test the echo endpoint
send_echo_request("Hello, Flask!")
send_echo_request("Say Phillip in French!")


#send_echo_request("This is a test prompt")

# Test with no message
#send_echo_request("")

# You can add more test cases here
#send_echo_request("who is the qb for the cowboys?")