# Copyright 2013 Rackspace Australia
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import testtools
import string
import random
import re

from fuzzy_happiness.randomise import random_char_replacement
from fuzzy_happiness.randomise import random_hexstring_replacement
from fuzzy_happiness.randomise import random_str_replacement
from fuzzy_happiness.randomise import random_pathname_replacement
from fuzzy_happiness.randomise import random_ipaddress_replacement


class TestRandomCharReplacement(testtools.TestCase):
    def test_simple_letter(self):
        for i in range(100):
            self.assertIn(random_char_replacement(
                random.choice(list(string.ascii_letters))),
                list(string.ascii_letters))

    def test_simple_digit(self):
        for i in range(100):
            self.assertIn(random_char_replacement(
                random.choice(list(string.digits))),
                list(string.digits))

    def test_simple_lc_letter(self):
        for i in range(100):
            self.assertIn(random_char_replacement(
                random.choice(list(string.ascii_lowercase))),
                list(string.ascii_lowercase))

    def test_simple_uc_letter(self):
        for i in range(100):
            self.assertIn(random_char_replacement(
                random.choice(list(string.ascii_uppercase))),
                list(string.ascii_uppercase))

    def test_simple_whitespace(self):
        for i in range(100):
            self.assertIn(random_char_replacement(
                random.choice(list(string.whitespace))),
                list(string.whitespace))

    def test_simple_symbols(self):
        for i in range(100):
            self.assertIn(random_char_replacement(
                random.choice(list('!@#$%^&*()_-~`"\',./<>?:;\\|[]{}'))),
                list('!@#$%^&*()_-~`"\',./<>?:;\\|[]{}'))


class TestRandomHexStringReplacement(testtools.TestCase):
    def test_happy_hex_day_single(self):
        allowable = list(string.hexdigits)
        new_str = random_hexstring_replacement("a")
        for i in new_str:
            self.assertIn(i, allowable)

    def test_happy_hex_day(self):
        allowable = list(string.hexdigits)
        new_str = random_hexstring_replacement("abc123")
        for i in new_str:
            self.assertIn(i, allowable)

    def test_happy_hex_day_letters(self):
        allowable = list(string.hexdigits)
        new_str = random_hexstring_replacement("def")
        for i in new_str:
            self.assertIn(i, allowable)

    def test_happy_hex_day_numbers(self):
        allowable = list(string.hexdigits)
        new_str = random_hexstring_replacement("768")
        for i in new_str:
            self.assertIn(i, allowable)


class TestRandomStrReplacement(testtools.TestCase):
    def test_simple(self):
        for i in range(100):
            for j in list(random_str_replacement("fred")):
                self.assertIn(j, string.ascii_letters)

    def test_big_sample(self):
        for i in range(100):
            strng = ""
            for j in range(random.randint(1, 1000)):
                strng += random.choice(string.letters)
            for k in list(random_str_replacement(strng)):
                self.assertIn(k, string.ascii_letters)

    def test_char(self):
        self.assertIn(random_str_replacement('q'), string.ascii_letters)

    def test_restricted_char(self):
        replacement_dict = {
            'numeric': (string.ascii_letters, list('c')),
        }
        self.assertIn(random_str_replacement('c', replacement_dict), 'c')

    def test_numbers(self):
        allowable = list(string.digits)
        replacement_dict = {
            'numeric': (string.ascii_letters, allowable),
        }
        new_str = random_str_replacement("foo", replacement_dict)
        for i in new_str:
            self.assertIn(i, allowable)

    def test_letters(self):
        allowable = list("jklmnop")
        replacement_dict = {
            'letters': (string.ascii_letters, allowable),
        }
        new_str = random_str_replacement("racoon", replacement_dict)
        for i in new_str:
            self.assertIn(i, allowable)


class TestRandomPathnameReplacement(testtools.TestCase):
    def test_file(self):
        possible_chars = (string.ascii_letters + string.digits +
                          '!@#$%^&*()_-~`"\',.<>?:;|[]{}')
        for i in range(100):
            new_str = random_pathname_replacement('foobar')
            for c in list(new_str):
                self.assertIn(c, possible_chars)

    def test_root(self):
        new_str = random_pathname_replacement('/')
        self.assertEqual(new_str, '/')

    def test_path(self):
        possible_chars = (string.ascii_letters + string.digits +
                          '!@#$%^&*()_-~`"\',.<>?:;|[]{}')
        for i in range(100):
            new_str = random_pathname_replacement('/foo/bar')
            self.assertIn(new_str[0], '/')
            self.assertIn(new_str[1], possible_chars)
            self.assertIn(new_str[2], possible_chars)
            self.assertIn(new_str[3], possible_chars)
            self.assertIn(new_str[4], '/')
            self.assertIn(new_str[5], possible_chars)
            self.assertIn(new_str[6], possible_chars)
            self.assertIn(new_str[7], possible_chars)


class TestRandomIPAddressReplacement(testtools.TestCase):
    def test_simple_ipv4(self):
        v4addr = re.compile(r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
                            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
                            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
                            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
        new_addr = random_ipaddress_replacement('192.168.1.6')
        self.assertTrue(v4addr.match(new_addr))
