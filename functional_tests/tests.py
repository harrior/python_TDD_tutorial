from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    """ new visitor test """

    def setUp(self) -> None:
        """install"""
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        """uninstall"""
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        """тест, что можно начать список и получить его позже"""
        # Пользователь заходит на главную струницу сайта со списками задач
        self.browser.get(self.live_server_url)

        # Он видит заголовок страницы To-Do list
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Ему сразу предлагают ввести новую задачу
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter to-do item')

        # Он вводит "Купить перья павлина"
        inputbox.send_keys('Купить перья павлина')
        # При нажатии Enter страница обновляется и теперь страница содержит "Купить перья павлина"
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить перья павлина')
        # Теперь он вводит "Сделать мушку из павлиньих перьев"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Сделать мушку из павлиньих перьев')
        inputbox.send_keys(Keys.ENTER)
        # Страница снова обновляется и теперь показывает два элемента его списка
        self.wait_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')
        self.wait_for_row_in_list_table('1: Купить перья павлина')

        # Сайт сгенерировал уникальный URL для этого списка?

        # Пользователь переходит по ссылке - список все еще на месте
        self.fail('Закончить тест!')

    def test_multiple_users_can_start_lists_at_different_url(self):
        ''' тест многочисленные юзеры могут начать свои списки по разным url'''
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить перья павлина')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить перья павлина')

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        # приходит новый юзер
        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить перья павлина', page_text)
        self.assertNotIn('Сделать мушку из павлиньих перьев', page_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить молоко')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')

        fransis_list_url = self.browser.current_url
        self.assertRegex(fransis_list_url, '/lists/.+')
        self.assertNotEqual(fransis_list_url, edith_list_url)

        page_text = self.browser.find_element_by_tag_name('body')
        self.assertNotIn('Купить перья павлина', page_text)
        self.assertIn('Купить молоко', page_text)
