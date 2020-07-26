TODO:

(on staging and then production)

* Push code
* Add weight attribute to product types (kg)
  * Weight (kg), weight, Float, Required=True
* Add weight value to all products
  * Hook: 0.025
  * Artisan: 0.11
  * Basic Shampoo: 0.10
  * Basic Soap: 0.09
* Create shipping methods in dashboard
  * Add default weight of 0.1 to all methods
* Edit "Delivery" page to explain shipping rates

Development needed:
* Display shipping method in orders list (dashboard)

WIP:

* Code pushed to staging
* Weight attribute added on staging
* Shipping methods being added on staging:
  * currently working on International Standard methods
  * use Django shell to copy country lists to new shipping methods
