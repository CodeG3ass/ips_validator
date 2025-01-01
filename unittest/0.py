import unittest
from unittest.mock import patch, MagicMock
import unittest
from test import *

class TestMyFunction(unittest.TestCase):

    @patch('tkinter.filedialog.askopenfilenames')
    @patch('tkinter.filedialog.asksaveasfilename')
    @patch('tkinter.Text')
    @patch('tkinter.Button')
    @patch('tkinter.Tk')
    def test_my_function(self, mock_tk, mock_button, mock_text, mock_asksaveasfilename, mock_askopenfilenames):
        # Создаем мок-объекты для GUI-компонентов
        mock_tk_instance = MagicMock()
        mock_button_instance = MagicMock()
        mock_text_instance = MagicMock()
        mock_asksaveasfilename.return_value = 'test.txt'
        mock_askopenfilenames.return_value = ['test1.txt', 'test2.txt']
        mock_tk.return_value = mock_tk_instance
        mock_button.return_value = mock_button_instance
        mock_text.return_value = mock_text_instance

        # Вызываем функцию
        my_function()

        # Проверяем, что функция вызвала ожидаемые методы
        mock_askopenfilenames.assert_called_once()
        mock_asksaveasfilename.assert_called_once()
        mock_tk_instance.mainloop.assert_called_once()

if __name__ == '__main__':
    unittest.main()
