from .base import FunctionalTest
from selenium import webdriver


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text  # 1
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        # She type "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers"  as an item in a to-do list
        self.get_input_element('Buy peacock feathers')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)
        self.get_input_element('Use peacock feathers to make a fly')

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # satisfied she can go back to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):

        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        self.get_input_element('Buy peacock feathers')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect
        # she notices that her list has a unique URL
        edit_list_url = self.browser.current_url
        self.assertRegex(edit_list_url, '/lists/.+')

        # Now a new user, Francis, comes along to the site

        ## We use a new browser session to make sure that no information
        ## of ediths is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page. There is no sign of edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new item.
        self.get_input_element('Buy milk')
        self.wait_for_row_in_list_table('1: Buy milk')

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edit_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep