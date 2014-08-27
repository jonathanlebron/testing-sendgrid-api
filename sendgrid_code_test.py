import sendgrid
import unittest
import logging
import sys

class TestSendgridAPI(unittest.TestCase):

    def setUp(self):
        sg_username = ""
        sg_password = ""

        self.sg = sendgrid.SendGridClient(sg_username, sg_password, raise_errors=True)

        self.to_email = "Someone Random <some_random_guy@email.com>"
        self.from_email = "Jonathan Lebron <jonathan.lebron@outlook.com>"
        self.cc_email = "Random CC <cc@email.com>"
        self.html = "<div style=\"background-color: #bbb; font-family: verdana, tahoma, sans-serif; color: #222; padding: 8px 25px; display:block; margin: 0 auto\"><h2>Hello Chris,</h2><p>This is a test message.</p><img src=\"http://upload.wikimedia.org/wikipedia/commons/5/52/Macaca_nigra_self-portrait.jpg\" height=\"480\" width=\"347\" alt=\"Macaque Selfie\" /><p>Thank you for checking out this cool selfie of a Macaque.</p><p>Love,<br/> Jonathan Lebron</p><img src=\"http://cdn1.sendgrid.com/images/sendgrid-logo.png\" alt=\"SendGrid!\" /></div>"

    def test_mail(self):
        message = sendgrid.Mail()
        message.add_to(self.to_email)
        message.set_from(self.from_email)
        message.set_subject("Testing Sendgrid API: Send Email")
        message.set_html(self.html)

        status, msg = self.sg.send(message)
        self.assertEqual(status, 200)

    def test_mail_with_cc(self):
        message = sendgrid.Mail()
        message.add_to(self.to_email)
        message.set_from(self.from_email)
        message.add_cc(self.cc_email) # adding cc
        message.set_subject("Testing Sendgrid API: Adding CC")
        message.set_html(self.html)

        status, msg = self.sg.send(message)
        self.assertEqual(status, 200)

    def test_mail_with_attachment(self):
        message = sendgrid.Mail()
        message.add_to(self.to_email)
        message.set_from(self.from_email)
        message.add_cc(self.cc_email)
        message.set_subject("Testing Sendgrid API: Attaching a File")
        message.set_html(self.html)
        message.add_attachment('stuff.txt', './stuff.txt') # adding attachment

        status, msg = self.sg.send(message)
        self.assertEqual(status, 200)

    def test_mail_with_error(self):
        message = sendgrid.Mail()
        message.add_to(self.to_email)
        message.set_from(self.from_email)
        message.add_cc(self.cc_email)
        message.set_subject("Testing Sendgrid API: Handling Errors")
        message.set_html(self.html.encode('bz2')) # using invalid encoding
        message.add_attachment('stuff.txt', './stuff.txt')

        with self.assertRaises(sendgrid.SendGridClientError):
            try:
                self.sg.send(message)
            except sendgrid.SendGridClientError as e:
                log = logging.getLogger("TestSendgridAPI.test_mail_with_error")
                log.debug("\nSendGridClientError: %s", e)
                raise e

if __name__ == '__main__':
    logging.basicConfig( stream=sys.stderr )
    logging.getLogger("TestSendgridAPI.test_mail_with_error").setLevel(logging.DEBUG)
    unittest.main()
