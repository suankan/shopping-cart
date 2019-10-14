from checkout import Checkout
from pricingrules import PricingRules

# Step 1: Create PricingRules object:
pricing_rules = PricingRules('/code/config/catalog.yaml',
    '/code/config/pricingrules.yaml')

# Step 2: Create Checkout object from previously created PricingRules objects.
checkout = Checkout(pricing_rules)

# Step 3: Scan a few SKUs
for sku in ['atv', 'atv', 'atv', 'vga']:
    checkout.scan(sku)

print(checkout.total())
