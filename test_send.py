from authenticate import authenticate
from Emailer import Emailer

gmail_service = authenticate()

emailer = Emailer()
message, body = emailer.get_welcome_msg("blah", "blah", "blah")

message = (gmail_service.users().messages().send(userId="me", body=body).execute())

