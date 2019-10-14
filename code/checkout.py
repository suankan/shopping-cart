'''
This module implements Checkout class according to this example:

The interface to our checkout looks like this (shown in java):

  Checkout co = new Checkout(pricingRules);
  co.scan(item1);
  co.scan(item2);
  co.total();
'''

from pricingrules import PricingRules

class Checkout:
    '''
    Scan products and calculate total.
    Each scanned product is added into a cart counting its quantity.

    Checkout is our shopping cart.
    Cart will be a dictionary with keys as Product SKUs and values as quantities.
    '''

    def __init__(self, pricing_rules):
        '''
        Initialise Checkout using pricing_rules object.
        There are some requirements to keep Checkout class interface.
        '''

        if not isinstance(pricing_rules, PricingRules):
            raise Exception('pricing_rules must be instance of PricingRules')

        self.selected_items = {}
        self.total_sum = 0
        self.pricing_rules = pricing_rules

    def scan(self, sku):
        '''
        This function takes SKU string and registers corresponding product
        as "selected for purchase" along with quantity.
        If a SKU has previously been scaned then it increments quantity.
        If a SKU is scanned first time then it sets quantity to 1.
        If a SKU is not in the products catalogue, then it throws exception.
        '''

        # Check if product sku is in catalog
        if sku not in self.pricing_rules.catalog:
            raise Exception('SKU not found in Catalog')

        # Set quantity to 1 if the product was not selected previously
        if sku not in self.selected_items:
            self.selected_items[sku] = {'quantity': 1}
        # Otherwise increment the quantity by 1
        else:
            self.selected_items[sku]['quantity'] += 1

    def total(self):
        '''
        This function calculates total sum of all scanned products according to their catalog price.
        TODO: to implement custom pricing rules (discounts)
        '''

        selected_skus = self.selected_items.keys()
        for sku in selected_skus:
            # Get price from catalog:
            price = self.pricing_rules.catalog[sku]['price']

            # Quantity of the product in the cart
            quantity = self.selected_items[sku]['quantity']

            self.total_sum += quantity * price

        # Search and apply discount for each selected sku
        total_discount_amount = 0
        for sku in selected_skus:
            if sku in self.pricing_rules.discounts:
                # WARNING: hashtag #uglycode
                # We have chosen to give Sales Manager an ability to manipulate
                # values in pricing rules on demand. E.g. in their pricingrules.yaml
                # they specify the name of the function which should implement certain discount.
                # Also they specify parameters for that discount function
                # e.g. target SKU to apply the discount to. As well as any additional
                # parameters required for the logic of this discount.
                # As a result, items in self.pricing_rules.discounts dict have a dict structure like:
                # 'func': {
                #     'name': '_discount_every_third_apple_tv',
                #     'params': {
                #         'appliedToSku': 'atv'
                #     }
                # }
                # This function has to be implemented inside PricingRules class and here we need to
                # execute it when we only have its name as a Python string.

                sku_discount = self.pricing_rules.discounts[sku]

                # Get discount function name and params
                func_name = sku_discount['func']['name']
                params = sku_discount['func']['params']

                # Execute obtained function
                # - against currently selected items
                # - using custom parameters passed by Sales Manager
                # - when only having its name as string.
                # Happy debugging.
                discount_function = getattr(self.pricing_rules, func_name)
                discount_amount = discount_function(self.selected_items, params)

                # Sum up the amount of all found discounts.
                total_discount_amount += discount_amount

                # Record the applied discount dict in the selected_items
                self.selected_items[sku]['discount'] = sku_discount

                # Record the applied discount amount in the selected_items dict
                self.selected_items[sku]['discount_amount'] = discount_amount

        return self.total_sum - total_discount_amount
