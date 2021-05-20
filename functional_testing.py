from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    """ new visitor test """

    def setUp(self) -> None:
        """install"""
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        """uninstall"""
        self.browser.quit()

    def test_can_start_a_list_and_retrive_it_later(self):
        """тест, что можно начать список и получить его позже"""
        # Пользователь заходит на главную струницу сайта со списками задач
        self.browser.get('http://127.0.0.1:8000')

        # Он видит заголовок страницы To-Do list
        self.assertIn('To-Do', self.browser.title)
        self.fail('Закончить тест!')

        # Ему сразу предлагают ввести новую задачу

        # Он вводит "Купить перья павлина"

        # При нажатии Enter страница обновляется и теперь страница содержит "Купить перья павлина"

        # Теперь он вводит "Сделать мушку из павлиньих перьев"

        # Страница снова обновляется и теперь показывает два элемента его списка

        # Сайт сгенерировал уникальный URL для этого списка?

        # Пользователь переходит по ссылке - список все еще на месте


if __name__ == '__main__':
    unittest.main()