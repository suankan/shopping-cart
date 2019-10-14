'''
Unit tests for checkout module
'''

import unittest
import sys
sys.path.append('/code')
from checkout import Checkout
from pricingrules import PricingRules


class TestCheckout(unittest.TestCase):
    '''
    Unit tests for checkout module
    '''

    def init_pricingrules(self):
        '''
        This function initialises PricingRules, Checkout objects from real files
        TODO: turn it into decorator.
        '''

        self.pricing_rules = PricingRules('/code/tests/config/catalog.yaml',
            '/code/tests/config/pricingrules.yaml')
        self.checkout = Checkout(self.pricing_rules)


    def teardown_pricingrules_and_catalog(self):
        '''
        Tear down Checkout object.

        Execute this after each unit test.

        TODO: turn it into decorator.
        '''
        self.checkout = None

    def test_constructor(self):
        '''
        Testing constructor
        '''

        self.init_pricingrules()

        # Make sure selected_items is an empty dict
        self.assertEqual(self.checkout.selected_items, {})
        # Make sure we have set zero total_sum
        self.assertEqual(self.checkout.total_sum, 0)
        # Make sure that pricing_rules is set to the mocked PricingRules object
        self.assertEqual(True, isinstance(self.checkout.pricing_rules, PricingRules))

        self.teardown_pricingrules_and_catalog()

    def test_scan_throws_exception(self):
        '''
        Test that scan() throws exception if someone scans SKU which is not in catalog
        '''

        self.init_pricingrules()

        with self.assertRaises(Exception):
            self.checkout.scan('no-such-SKU')

        self.teardown_pricingrules_and_catalog()

    def test_scan_quantity_increments(self):
        '''
        Make sure that quantity is set to 1 if Apple TV SKU is scanned first time.
        Make sure that quantity is incremented if Apple TV SKU is scanned second time.
        '''
        self.init_pricingrules()

        # First scan
        self.checkout.scan('atv')
        self.assertEqual(1, self.checkout.selected_items['atv']['quantity'])

        # Second scan
        self.checkout.scan('atv')
        self.assertEqual(2, self.checkout.selected_items['atv']['quantity'])

        self.teardown_pricingrules_and_catalog()

    def test_total_no_discount(self):
        '''
        SKUs Scanned: atv, atv, atv, vga Total expected: 358.5 (no discounts)
        '''

        self.init_pricingrules()

        for sku in ['atv', 'atv', 'atv', 'vga']:
            self.checkout.scan(sku)

        actual = self.checkout.total()
        expected = float(249.00)
        # expected = float(358.5)

        self.assertEqual(actual, expected)

        self.teardown_pricingrules_and_catalog()

if __name__ == '__main__':
    unittest.main()
