from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()


    def test_can_start_a_list_and_retrieve_it_later(self):

            # Edith has heard about a cool new online to-do app. She goes
            # to check out its homepage
            self.browser.get('http://localhost:8000')

            # She notices the page title and header mention to-do lists
            self.assertIn('To-Do', self.browser.title)
            header_text = self.browser.find_element_by_tag_name('h1').text #1
            #self.fail('Finish the test!')

            # She is invited to enter a to-do item straight away
            input_box = self.browser.find_element_by_id('item_text') #1
            self.assertEqual(
                input_box.get_attribute('placeholder'),
                'Enter a to-do item'
            )


            # She type "Buy peacock feathers" into a text box (Edith's hobby
            # is tying fly-fishing lures)
            input_box.send_keys('Buy peacock feathers') #2

            # When she hits enter, the page updates, and now the page lists
            # "1: Buy peacock feathers"  as an item in a to-do list
            input_box.send_keys(Keys.ENTER) #3
            time.sleep(1) #4

            table = self.browser.find_element_by_id('id_list_table')
            rows = table.find_elements_by_tag_name('tr') #1
            self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
            self.assertIn('2: Use peacock feather to make a fly', [row.text for row in rows])
            # self.assertTrue(
            #     any(row.text == '1: Buy peacock feather' for row in rows),
            #     f"New to-do item did not appear in table. Contents were:\n{table.text}"
            # )

            # There is still a text box inviting her to add another item. She
            # enters "Use peacock feathers to make a fly" (Edith is very methodical)
            self.fail('Finish the test')

            # The page updates again, and now shows both items on her list

            # Edith wonders whether the site will remember her list. Then she sees
            # that the site has generated a unique URL for her -- there is some
            # explanatory text to that effect

            # She visits that URL - her to-do list is still there.

            # Satisfied, she goes back to sleep



if __name__ == '__main__':
    unittest.main(warnings='ignore')