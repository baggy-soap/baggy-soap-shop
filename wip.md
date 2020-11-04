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
* Ensure all countries are set to shippable
* Migrate (update to Order model)

WIP:

* Push mgmt command code to staging
* Weight attribute added on staging
* Shipping methods being added on staging:
  * currently working on International Standard methods
  * use Django shell to copy country lists to new shipping methods (including UK?) >> perhaps no longer needed with mgmt command
  * need to set countries as shippable on staging >> could be done by mgmt command?
  
  
  
Model changes: 

Migrations for 'order':
  custom_apps/order/migrations/0008_order_package_count.py
    - Add field package_count to order
