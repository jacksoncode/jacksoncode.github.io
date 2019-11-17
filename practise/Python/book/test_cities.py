# test_cities.py
import unittest
from cite_functions import get_formatted_city

class CitiesTestCase(unittest.TestCase):
    
    def test_city_country(self):
        formatted_city = get_formatted_city('Shanghai', 'China')
        self.assertEqual(formatted_city, 'Shanghai, China')

unittest.main()