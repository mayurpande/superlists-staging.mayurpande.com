from contextlib import contextmanager

from django.core import mail

from selenium.webdriver.common.keys import Keys
import re
import os
import poplib
import time

from .base import FunctionalTest

TEST_EMAIL = os.environ['TEST_USER_LOGIN']
SUBJECT = 'Your login link for superlists'


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):


        # Edith goes to the awesome superlists site
        # and notices a "log in" section in the navbar for the first time
        # It's telling her to enter her email address, so she does
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # A message appears telling her an email has been sent
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text
        ))

        # she checks her email and finds a message
        # email = mail.outbox[0]
        # self.assertIn(TEST_EMAIL, email.to)
        # self.assertEqual(email.subject, SUBJECT)
        body = self.wait_for_email(TEST_EMAIL, SUBJECT)

        # It has a url link in it
        # self.assertIn('use this link to login', email.body)
        # url_search = re.search(r'http://.+/.+$', email.body)
        self.assertIn('use this link to login:', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            # self.fail(f'Could not find url in email body:\n{email.body}')
            self.fail(f'Could not find url in email body:\n{body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # she clicks it
        self.browser.get(url)

        # she is logged in!
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        # Now she logs out
        self.browser.find_element_by_link_text('Log out').click()

        # She is logged out
        self.wait_to_be_logged_out(email=TEST_EMAIL)

    @contextmanager
    def pop_inbox(self):
        inbox = poplib.POP3_SSL('pop.gmail.com', '995')
        inbox.user(TEST_EMAIL)
        inbox.pass_(os.environ.get('TEST_USER_PASSWORD'))
        try:
            yield inbox
        finally:
            inbox.quit()

    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        last_count = 0
        start = time.time()
        while time.time() - start < 60:
            with self.pop_inbox() as inbox:
                count, _ = inbox.stat()
                if count != last_count:
                    for i in range(count, last_count, -1):
                        resp, lines, octets = inbox.retr(i)
                        try:
                            lines = [l.decode('utf-8') for l in lines]
                            if f'Subject: {subject}' in lines:
                                inbox.dele(i)
                                return '\n'.join(lines)
                        except:
                            continue
                    last_count = count
            time.sleep(5)
