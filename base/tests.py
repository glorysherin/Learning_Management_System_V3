# a = [	
#     '00011111',
# 	'00010001',
# 	'00010011',
# 	'00010110',
# 	'00011100',
# 	'00010000',
# 	'00011111',
# 	'00000000']


# b = [ int(i) for i in "1,2,8,16,32,64,128".split(',')[::-1] ]

# print(b)

# sum = 0

# out = []

# for i in a: 
#     for k,j in enumerate(i):
#         if int(j) == 1:
#             print(sum,k)
#             sum = sum + b[k-1]
#     out.append(sum)

# print(out)



# import requests
# from bs4 import BeautifulSoup


# def google_search(query):
#     url = f"https://www.google.com/search?q={query}"
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.content, "lxml")
#     search_results = []
#     for result in soup.find_all("div", class_="g"):
#         link = result.find("a").get("href")
#         title = result.find("h3").text
#         description = result.find("span", class_="aCOpRe").text
#         search_results.append((title, link, description))
#     return search_results


# google_search("cat")


# from django.core.mail import send_mail

# send_mail(
#     'Notification Subject',
#     'Notification Message',
#     'sender@example.com',
#     ['recipient@example.com'],
#     fail_silently=False,
# )

# import ESL

# # Define FreeSWITCH connection details
# fs_host = 'localhost'
# fs_port = 8021
# fs_password = 'ClueCon'

# # Establish a connection to FreeSWITCH
# con = ESL.ESLconnection(fs_host, fs_port, fs_password)

# # Check if the connection is successful
# if con.connected():
#     print('Connected to FreeSWITCH')

#     # Define the call destination and parameters
#     destination = 'user/1000'
#     caller_id = '1001'
#     timeout = '30'

#     # Originate the call
#     con.api('originate', f'sofia/internal/{destination} &bridge(sofia/internal/{caller_id})', timeout)

#     # Wait for the call to be answered
#     event = con.recvEvent()
#     if event and event.get('Event-Name') == 'CHANNEL_ANSWER':
#         print('Call answered')
#     else:
#         print('Call not answered')

#     # Hang up the call
#     con.api('uuid_kill', event.get('Unique-ID'))

# # Disconnect from FreeSWITCH
# con.disconnect()




# from CC.modem import GsmModem

# def send_sms(port, baudrate, recipient, message):
#     # Initialize the GSM modem
#     modem = GsmModem(port, baudrate)

#     try:
#         # Connect to the modem
#         modem.connect()

#         if modem.is_connected():
#             print("Connected to GSM modem")

#             # Send the SMS
#             modem.send_sms(recipient, message)

#             print("SMS sent successfully")
#         else:
#             print("Failed to connect to GSM modem")
#     except Exception as e:
#         print("An error occurred:", str(e))
#     finally:
#         # Disconnect from the modem
#         modem.disconnect()

# # Configure the GSM modem and SMS details
# port = '/dev/ttyUSB0'  # Replace with the appropriate serial port
# baudrate = 115200  # Replace with the appropriate baud rate
# recipient = '+917401268091'  # Replace with the recipient's phone number
# message = 'Hello, this is a test SMS'

# # Send the SMS
# send_sms(port, baudrate, recipient, message)


