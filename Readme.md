# Purpose

This is implementation of [these requirements](https://github.com/DiUS/coding-tests/blob/master/dius_shopping.md)

The artifact of this solution will be a docker image with everything inside.

# How to build this code

To build docker image you need to

- Clone this repo and step into the repo directory.
- Then run this command.

```bash
$ docker build -t shopping-cart .
Sending build context to Docker daemon  93.18kB
Step 1/3 : FROM python:alpine
 ---> 39fb80313465
Step 2/3 : COPY ./code /code
 ---> c44b673b614a
Step 3/3 : WORKDIR /code
 ---> Running in 304a7381af18
Removing intermediate container 304a7381af18
 ---> da045272a697
Successfully built da045272a697
Successfully tagged shopping-cart:latest
```

# How to run unit tests

Using the image you've just build, execute unit tests:

```bash
$ docker run -it --rm --name shopping-cart shopping-cart python3 -m unittest discover -s tests -p '*_test.py' -v
test_constructor (checkout_test.TestCheckout) ... ok
test_scan_quantity_increments (checkout_test.TestCheckout) ... ok
test_scan_throws_exception (checkout_test.TestCheckout) ... ok
test_total_no_discount (checkout_test.TestCheckout) ... ok
test_discount_every_third_apple_tv_bought_3 (pricingrules_test.TestPricingRules) ... ok
test_discount_every_third_apple_tv_bought_4 (pricingrules_test.TestPricingRules) ... ok
test_discount_every_third_apple_tv_bought_5 (pricingrules_test.TestPricingRules) ... ok
test_discount_every_third_apple_tv_bought_7 (pricingrules_test.TestPricingRules) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.057s

OK
```

# How to use this code

## Sales Manager sets prices and pricing rules

This is done by editing YAML files inside ./config directory.

NOTE! Don't modify `.yaml` files inside `/code/tests/config/catalog.yaml`. Because they are used as unit tests fixtures and unit tests will be broken if you change them.

### File `/code/config/catalog.yaml`

This files represents a set of Products

```yaml
---
kind: Product
sku: ipd
name: Super iPad
price: 549.99
```

You can multiply and copy-paste these Product blocks as long as you keep SKUs unique.

You can set values of sku, name, price to whatever you want.

NOTE! negative prices have not been tested!

### File `/code/config/pricingrules.yaml`

This file represents a set of PricingRules.

```yaml
---
kind: PricingRule
name: get-three-apple-tv-for-price-of-two
description: we are going to have a 3 for 2 deal on Apple TVs. For example, if you buy 3 Apple TVs, you will pay the price of 2 only
func:
  name: discount_every_third
  params:
    appliedToSku: atv
```

You can copy-paste these PricingRule blocks.
All func names which you use in pricingrules.yaml must be implemented in PricingRule python class.

That leads to a workflow:

- Sales Manager drafts/models the pricing rule in YAML.
- Then Developer can pick up the YAML file and implement corresponding function in PricingRule python class.

In the YAML it is:
- possible to specify function name and parameters required for the logic of this pricing rule.
- parameter `appliedToSku` is mandatory.
- for any given `appliedToSku` parameter there can be only one PricingRule in the whole YAML.

## Developer implements new pricing rule

See example implementation and documentation for `PricingRules.discount_every_third()` and `Checkout.total()` functions.


# Example script

See `run.py`
