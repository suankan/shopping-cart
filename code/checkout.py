'''
This module implements Checkout class according to this example:

The interface to our checkout looks like this (shown in java):

  Checkout co = new Checkout(pricingRules);
  co.scan(item1);
  co.scan(item2);
  co.total();
'''

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

        # Increment quantity if the product is already in the cart
        if sku in self.selected_items:
            self.selected_items[sku] += 1
        # Otherwise set quantity to 1
        else:
            self.selected_items[sku] = 1

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
            quantity = self.selected_items[sku]

            self.total_sum += quantity * price

        return self.total_sum
