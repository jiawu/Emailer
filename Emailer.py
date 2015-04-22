import base64
from email.mime.text import MIMEText
import pandas as pd
import pdb
import re
import math
class Emailer:
    def __init__(self):
       self.matches = None
       self.self_addr = "nulinklunch@gmail.com"
       self.template_file = "template.txt"
      # self.alwayscc = ''
       self.alwayscc = 'austinisner2012@u.northwestern.edu, zafirzaman2015@u.northwestern.edu'
       self.default_subject = "[NU-LinkLunch] LinkLunch Match!"

    def get_matches(self,match_xls, address_xls):
        #gets a list of matches which is a list of dicts
        self.email_table = pd.read_excel(address_xls, index_col = None, na_values=['NA'])
        self.match_table = pd.read_excel(match_xls, index_col = None)

        self.email_table = self.email_table.reset_index()
        self.match_table = self.match_table.reset_index()
        match = self.match_table
        #for each row in the match table, generate a list of matches

        matches = []

        for index, row in self.match_table.iterrows():

            match1_name = row['Match1']
            match2_name = row['Match2']

            match_dict = {  'match1': match1_name,
                            'match2': match2_name,
                            'match1_email': self.get_email(match1_name),
                            'match2_email': self.get_email(match2_name),
                            'match1_dept': self.get_dept(match1_name),
                            'match2_dept': self.get_dept(match2_name),
                            'based_on': row['Mutual_Interest_In'],
                            'chicago': row['Chicago'],
                            'which_person_chicago': row['Which_Person_Chicago'],
                            'notified':row['Notified?'],
                            'additional':row['Additional_Note']
                        }
            matches.append(match_dict)


        return(matches)

    def get_template(self):
        with open(self.template_file) as fi:
            data=fi.read()
        return(data)
    def replace_text(self, match_dict, template):
        if type(match_dict['additional']) is float:
            if math.isnan(match_dict['additional']):
                match_dict['additional'] = ''
        string ='!|!'.join(map(re.escape,match_dict))
        string = '!' + string + '!'
        rc = re.compile(string)
        def translate(match):
            astr = str(match.group(0)).replace("!","").replace("!","")
            return match_dict[astr]
        return(rc.sub(translate,template))


    def get_dept(self, name):
        email = ''
        try:
            email = self.email_table[self.email_table['Full Name'].str.contains(name)].iloc[0]['Department/Program']
            email = str(email)
        except IndexError:
            print 'cannot find email',name
            raise
        return(email)

    def get_email(self, name):
        email = ''
        try:
            email = self.email_table[self.email_table['Full Name'].str.contains(name)].iloc[0]['Email']
            email = str(email)
        except IndexError:
            print 'cannot find email',name
            raise
        return(email)

    def get_welcome_email(self,match_dict, body):
        # create a message to send
        message = MIMEText(body, 'html', 'utf-8')
        send_to = str(match_dict['match1_email']) + ',' + str(match_dict['match2_email'])
        message['to'] = send_to
        message['cc'] = self.alwayscc
        message['from'] = self.self_addr
        message['subject'] = self.default_subject
        body = {'raw': base64.b64encode(message.as_string())}
        return((message,body))

