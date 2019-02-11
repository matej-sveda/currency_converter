import unittest
from converter import error_msg, check_currency, convert_to_all, convert_between
import json

class TestCurrencyConverter(unittest.TestCase):
    def test_error_msg(self):
        self.assertEqual(error_msg('SomeError', "This is wrong!"), json.dumps({'SomeError': "This is wrong!"}))

    def test_check_currecy(self):
        self.assertEqual(check_currency('CHF'), 'CHF')
        self.assertEqual(check_currency('US$'), 'USD')
        self.assertEqual(check_currency('chf'), json.dumps({'Error': "Entered currency code or symbol not found! "
                                                                        "Mind the upper casing!"}))

    def test_convert_to_all(self):
        self.assertEqual(convert_to_all(-1, 'CZK'), error_msg('Error', "Amount has to be a number greater than zero!"))
        self.assertEqual(convert_to_all(1, 5), error_msg('Error', "Entered currency code or symbol not found! "
                                                                         "Mind the upper casing!"))
        self.assertEqual(convert_to_all(1, 'usd'), error_msg('Error', "Entered currency code or symbol not found! "
                                                                         "Mind the upper casing!"))
        self.assertEqual(convert_to_all(1, '¥'), (convert_to_all(1, 'JPY')))

    def test_convert_between(self):
        self.assertEqual(convert_to_all(-1, 'CZK'), error_msg('Error', "Amount has to be a number greater than zero!"))
        self.assertEqual(convert_between(1, 5, 'JPY'), error_msg('Error', "Entered currency code or symbol not found! "
                                                                          "Mind the upper casing!"))
        self.assertEqual(convert_between(1, 'CZK', ':'), error_msg('Error', "Entered currency code or symbol not found! "
                                                                            "Mind the upper casing!"))
        self.assertEqual(convert_between(1, 'usd', 'nok'), error_msg('Error', "Entered currency code or symbol not found! "
                                                                            "Mind the upper casing!"))
        self.assertEqual(convert_between(10, 'Kč', 'Nkr'), convert_between(10, 'CZK', 'NOK'))

if __name__ == '__main__':
    unittest.main()

