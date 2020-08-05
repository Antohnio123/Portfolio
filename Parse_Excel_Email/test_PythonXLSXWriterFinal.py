import unittest
from PythonXLSXWriterFinal import cut, scrapper, excelwork, sendmessage, RESULTFILE, worksheetName
from openpyxl import Workbook, load_workbook


class Currencytest(unittest.TestCase):
    T = scrapper('https://yandex.ru/news/quotes/2002.html')
    def test_scrapper(self):  # Работает
        self.assertIsNotNone(self.T)
        self.assertIsInstance(self.T, tuple)
        self.assertIsInstance(self.T[1][1], float)
        self.assertIsInstance(self.T[2][9], float)

    def test_excel(self):
        excelwork(RESULTFILE, worksheetName, self.T, self.T)
        self.wb = load_workbook(filename=RESULTFILE, data_only=True)
        self.sheet_ranges=self.wb[worksheetName]
        self.assertIsInstance(self.sheet_ranges['B9'].value, float)
        self.assertIsInstance(self.sheet_ranges['C9'].value, float)
        self.assertIsInstance(self.sheet_ranges['G9'].value, int or float)

    def test_email(self):




    # def test_NonValidInput_negative(self):  # Прогоняет верно, но сам этого не видит.
    #     self.assertRaises(NonValidInput, to_roman, '-1')
    #
    # def test_NonValidInput_limit(self):  # Прогоняет верно, но сам этого не видит.
    #     t = str(40000)
    #     print(t)
    #     self.assertRaises(NonValidInput, to_roman, t)
    #
    # def test_result_7000(self):  # Работает
    #     self.assertEqual('IƆƆCIƆCIƆ', to_roman(7000))


if __name__ == '__main__':
    unittest.main()