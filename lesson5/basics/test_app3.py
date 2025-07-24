from app3 import send_chat_request

# Test the echo endpoint
send_chat_request("say hi in french")
#Server responded: {'suggestions': 'Bonjour!'}

print("")
send_chat_request("say hi Phillip in french and in binary")
# Server responded: {'suggestions': 'Bonjour, Phillip! (French)\n\n01101000 01101001 00100000 01010000 01101000 01101001 01101100 01101100 01101001 01110000 (Binary)'}