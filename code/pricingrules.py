'''
This module implements loading pricing rules and catalog from YAML files.
In the requirements it was outlined that Sales Manager might want to update
prices and pricing rules with a very short notice.

For that, we will show Sales Manager how to keep prices in YAML and
store them in version control for future reference.

Sales Manager be able to:
- edit prices anytime by editing YAML files.
- chuck them into version control

Shopping selected_items developers will be able to:
- pick the catalog and pricing rules from YAML files
- load them into the shopping selected_items application
'''

import yaml
from math import floor

class PricingRules():
    '''
    This class is initialised by two YAML files: catalog and pricingrules.
    Constructor reads YAML files and the data in the class members.
    '''

    def __init__(self, catalog_file, pricing_rules_file):

        # Load catalog from yaml
        self.catalog = {}
        with open(catalog_file) as f:
            catalog_products = yaml.load_all(f, Loader=yaml.Loader)
            for product in catalog_products:
                sku = product['sku']
                self.catalog[sku] = product

        # Load pricing rules from yaml
        self.discounts = {}
        with open(pricing_rules_file) as f:
            rules = yaml.load_all(f, Loader=yaml.Loader)
            for rule in rules:
                sku = rule['func']['params']['appliedToSku']
                self.discounts[sku] = rule

    def discount_every_third(self, selected_items, params):
        '''
        This function implements quantity manipulation
        on the given SKU in the given shopping selected_items.

        Input:
            selected_items: here we expect a dict of skus and their quantities.
                For example:
                    {'sku1': 'quantity1',
                    'sku2':  'quantity2',
                    'sku3':  'quantity3'}

            params: actual parameters for this function.
                This is a dict with a structure from pricingrules.yaml.
                For example:
                    {'appliedToSku':    'atv',
                    'param_A':          'value_A',
                    'param_B':          'value_B'}

        Returns: dollars amount of discount

        Example of quantity manipulation:

        3 turns into 2
        6 turns into 4
        9 turns into 6
        and so on.

        So we discount every third item.
         '''

        if 'appliedToSku' not in params:
            # This indicates that func params were specified in YAML without key appliedToSku'
            raise Exception('Param appliedToSku must always be specified in PricingRules YAML')

        # Which SKU should it be applied:
        sku = params['appliedToSku']

        if sku in selected_items:
            quantity = selected_items[sku]['quantity']
            # This will be the number of full triplets of the same SKU added into the selected_items.
            number_of_discounted_items = floor(quantity/3)

            # Lookup for the catalog price of this SKU
            price = self.catalog[sku]['price']
            discount_amount = number_of_discounted_items * price

            return discount_amount

