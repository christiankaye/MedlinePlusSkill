# -*- coding:utf-8 -*-

import os
import shutil
import unittest
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from delver import Crawler

class TestAll(unittest.TestCase):

    def setUp(self):
        self.urls = {
            'FORM2': 'https://medlineplus.gov/'
        }
        self.urls_list = [
            "https://medlineplus.gov/"
        ]
        
    def test_submit_query(self):
        c = Crawler()
        response = c.open('https://medlineplus.gov/')
        self.assertEqual(response.status_code, 200)
        forms = c.forms(filters={'id': 'mplus-search'})
        search_form = forms[0]
        search_form.fields = {
            'query': """
        }
        c.submit(search_form)
        success_check = c.submit_check(
            search_form,
            phrase= """,
            status_codes=[200]
        )
        print(success_check)
        
        self.assertEqual(search_form.fields['query'].get('value'), """)

    def test_crawler_scraper_methods(self):
        c = Crawler()
        c.logging = True
        c.useragent = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        c.open("https://vsearch.nlm.nih.gov/vivisimo/cgi-bin/query-meta?v%3Aproject=medlineplus&v%3Asources=medlineplus-bundle&query=["""]")
        p_text = c.xpath('//*[@id="document-list"]/div[1]/div[2]/div[2]/p[1]')

if __name__ == '__main__':
    unittest.main()
