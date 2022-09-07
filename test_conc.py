import unittest
import conccurency as conc


class TestConc(unittest.TestCase):

    def test_one(self):

        result = conc.get_url_list()
        self.assertTrue(type(result) is list)

    


    
unittest.main()