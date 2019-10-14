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

Using the image you've just build, eecute unit tests:

```bash
$ docker run -it --rm --name shopping-cart shopping-cart python3 checkout_test.py -v
test_constructor (__main__.TestPricingRules) ... ok
test_scan_quantity_increments (__main__.TestPricingRules) ... ok
test_scan_throws_exception (__main__.TestPricingRules) ... ok
test_total_no_discount (__main__.TestPricingRules) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.001s

OK
```