'''
Unit tests for pricingrules module
'''

import unittest
import sys
sys.path.append('/code')
from checkout import Checkout
from pricingrules import PricingRules

class TestPricingRules(unittest.TestCase):
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

    def test_discount_every_third_apple_tv_bought_3(self):
        '''
        Testing pricing rule discount_every_third when buying 3 Apple TVs and one VGA.
        SKUs Scanned: atv, atv, atv, vga
        Total expected: $249.00
        '''

        self.init_pricingrules()

        for sku in ['atv', 'atv', 'atv', 'vga']:
            self.checkout.scan(sku)

        #
        self.assertEqual(249.00, self.checkout.total())

        self.teardown_pricingrules_and_catalog()

    def test_discount_every_third_apple_tv_bought_4(self):
        '''
        Testing pricing rule discount_every_third when buying 4 Apple TVs and one VGA.
        Make sure that discount_every_third pricing rule works fine on Apple TV.
        SKUs Scanned: atv, atv, atv, atv, vga
        Total expected: 109.50 * 4 - 109.50 + 30.00 = $358.5
        '''

        self.init_pricingrules()

        for sku in ['atv', 'atv', 'atv', 'atv', 'vga']:
            self.checkout.scan(sku)

        #
        self.assertEqual(109.50 * 4 - 109.50 + 30.00, self.checkout.total())

        self.teardown_pricingrules_and_catalog()

    def test_discount_every_third_apple_tv_bought_5(self):
        '''
        Testing pricing rule discount_every_third when buying 5 Apple TVs and one VGA.
        Make sure that discount_every_third pricing rule works fine on Apple TV.
        SKUs Scanned: atv, atv, atv, atv, atv, vga
        Total expected: 109.50 * 5 - 109.50 + 30.00 = $468.0
        '''

        self.init_pricingrules()

        for sku in ['atv', 'atv', 'atv', 'atv', 'atv', 'vga']:
            self.checkout.scan(sku)

        #
        self.assertEqual(109.50 * 5 - 109.50 + 30.00, self.checkout.total())

        self.teardown_pricingrules_and_catalog()

    def test_discount_every_third_apple_tv_bought_7(self):
        '''
        Testing pricing rule discount_every_third when buying 5 Apple TVs and one VGA.
        Make sure that discount_every_third pricing rule works fine on Apple TV.
        SKUs Scanned: atv, atv, atv, atv, atv, atv, atv, vga
        Total expected: 109.50 * 7 - 109.50 * 2 + 30.00 = $687.0
        '''

        self.init_pricingrules()

        for sku in ['atv', 'atv', 'atv', 'atv', 'atv', 'atv', 'atv', 'vga']:
            self.checkout.scan(sku)

        self.assertEqual(109.50 * 7 - 109.50 * 2 + 30.00, self.checkout.total())

        self.teardown_pricingrules_and_catalog()


if __name__ == '__main__':
    unittest.main()
