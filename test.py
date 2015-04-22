import unittest
import pdb
from authenticate import authenticate
from Emailer import Emailer

class testSend(unittest.TestCase):
    def setUp(self):
        self.gmail_service = authenticate()
        self.emailer = Emailer()
        self.match_xls = '/Users/jjw036/Dropbox/GSA/LinkLunch/matches_04212015.xlsx'
        self.address_xls = '/Users/jjw036/Dropbox/GSA/LinkLunch/individual_info.xlsx'

    def test_template(self):
        template_txt = self.emailer.get_template()
        pdb.set_trace()
        test_dict = { 'match1': 'Jia Awesomepants',
                            'match2': 'Bruce Wayne',
                            'match1_email': 'jiawu@u.northwestern.edu',
                            'match2_email': 'mvjulia.wu@gmail.com',
                            'match1_dept': 'Magic',
                            'match2_dept': 'Crime Fighting',
                            'based_on': 'cheese',
                            'chicago': 'Y',
                            'which_person_chicago': 'Bruce',
                            'notified':'N',
                            'additional':'Take note that Bruce\'s batcave is located on the Chicago campus.'}
        new_body = self.emailer.replace_text(test_dict,template_txt)
        message, body = self.emailer.get_welcome_email(test_dict, new_body)
        message = (self.gmail_service.users().messages().send(userId="me", body=body).execute())


    def test_get_matches(self):
        match_list = self.emailer.get_matches(self.match_xls, self.address_xls)

    def test_get_email(self):
        match_list = self.emailer.get_matches(self.match_xls, self.address_xls)
        email_add = self.emailer.get_email('Ivy')
        self.assertEquals(email_add, 'ivynch@u.northwestern.edu')

    def test_send(self):
        pass
if __name__ == '__main__':
    unittest.main()
