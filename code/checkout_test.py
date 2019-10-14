'''
Unit tests for checkout module
'''

import unittest
from unittest.mock import Mock
from checkout import Checkout

class TestPricingRules(unittest.TestCase):
    '''
    Unit tests for checkout module
    '''

    def mock_pricingrules_and_catalog(self):
        '''
        Mock prerequisites for Checkout class and create Checkout object

        Execute this before each unit test.

        According to spec, Checkout class should be initialised by pricing_rules object.
        We will plan implementation of pricing_rules object so that it will know
        about catalog and discounts (pricing rules).

        TODO: turn it into decorator.
        '''

        # We will have to mock pricing_rules to test the exception
        self.pricing_rules = Mock()

        # Mock the catalog as dict
        self.pricing_rules.catalog = {
            'atv': {
                'kind': 'Product',
                'name': 'Apple TV',
                'price': 109.5,
                'sku': 'atv'
            },
            'ipd': {
                'kind': 'Product',
                'name': 'Super iPad',
                'price': 549.99,
                'sku': 'ipd'
            },
            'mbp': {
                'kind': 'Product',
                'name': 'MacBook Pro',
                'price': 1399.99,
                'sku': 'mbp'
            },
            'vga': {
                'kind': 'Product',
                'name': 'VGA adapter',
                'price': 30.0,
                'sku': 'vga'
            }
        }

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

        self.mock_pricingrules_and_catalog()

        # Make sure selected_items is an empty dict
        self.assertEqual(self.checkout.selected_items, {})
        # Make sure we have set zero total_sum
        self.assertEqual(self.checkout.total_sum, 0)
        # Make sure that pricing_rules is set to the mocked PricingRules object
        self.assertEqual(True, isinstance(self.checkout.pricing_rules, Mock))

        self.teardown_pricingrules_and_catalog()

    def test_scan_throws_exception(self):
        '''
        Test that scan() throws exception if someone scans SKU which is not in catalog
        '''

        self.mock_pricingrules_and_catalog()

        with self.assertRaises(Exception):
            self.checkout.scan('no-such-SKU')

        self.teardown_pricingrules_and_catalog()

    def test_scan_quantity_increments(self):
        '''
        Make sure that quantity is set to 1 if Apple TV SKU is scanned first time.
        Make sure that quantity is incremented if Apple TV SKU is scanned second time.
        '''
        self.mock_pricingrules_and_catalog()

        # First scan
        self.checkout.scan('atv')
        self.assertEqual(1, self.checkout.selected_items['atv'])

        # Second scan
        self.checkout.scan('atv')
        self.assertEqual(2, self.checkout.selected_items['atv'])

        self.teardown_pricingrules_and_catalog()

    def test_total_no_discount(self):
        '''
        SKUs Scanned: atv, atv, atv, vga Total expected: 358.5 (no discounts)
        '''

        self.mock_pricingrules_and_catalog()

        for sku in ['atv', 'atv', 'atv', 'vga']:
            self.checkout.scan(sku)

        actual = self.checkout.total()
        # expected = float(249.00)
        expected = float(358.5)

        self.assertEqual(actual, expected)

        self.teardown_pricingrules_and_catalog()

if __name__ == '__main__':
    unittest.main()
