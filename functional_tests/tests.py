from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(LiveServerTestCase):
    """ new visitor test """

    def setUp(self) -> None:
        """install"""
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        """uninstall"""
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrive_it_later(self):
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
        time.sleep(1)
        self.check_for_row_in_list_table('1: Купить перья павлина')
        # Теперь он вводит "Сделать мушку из павлиньих перьев"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Сделать мушку из павлиньих перьев')
        inputbox.send_keys(Keys.ENTER)
        # Страница снова обновляется и теперь показывает два элемента его списка
        time.sleep(1)
        self.check_for_row_in_list_table('1: Купить перья павлина')
        self.check_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')

        # Сайт сгенерировал уникальный URL для этого списка?

        # Пользователь переходит по ссылке - список все еще на месте
        self.fail('Закончить тест!')

