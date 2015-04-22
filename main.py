from Emailer import Emailer
from authenticate import authenticate
import pdb
# send it
try:

    match_xls = '/Users/jjw036/Dropbox/GSA/LinkLunch/matches_04212015.xlsx'
    address_xls = '/Users/jjw036/Dropbox/GSA/LinkLunch/individual_info.xlsx'
    gmail_service = authenticate()
    emailer = Emailer()

    matches = emailer.get_matches(match_xls, address_xls)
    #parse the list of matches
    #matches is a list of dicts
    for match in matches:
        template = emailer.get_template()
        new_body = emailer.replace_text(match,template)

        message, body = emailer.get_welcome_email(match,new_body)
        print(new_body)
        user_confirmation = raw_input('Send this email? (1 Y/ 2 n/ 3s) ')
        if float(user_confirmation) == 1:
            message = (gmail_service.users().messages().send(userId="me", body=body).execute())

            print('Message Id: %s' % message['id'])
            print(message)

        elif float(user_confirmation) == 2:
            break

        elif float(user_confirmation) == 3:
            continue

except Exception as error:
    print('An error occurred: %s' % error)

