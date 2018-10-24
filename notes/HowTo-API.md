# API


----

#### returns list of years
[http://bootcamp.brogard.io:5051/years](http://bootcamp.brogard.io:5051/years)

----

#### returns categories for a specific year
- parameter(s):
  - _{year}_

`http://bootcamp.brogard.io:5051/categories/{year}/year`

>example:

[http://bootcamp.brogard.io:5051/categories/2015/year](http://bootcamp.brogard.io:5051/categories/2015/year)

----

#### returns ads for a specific category and year
- parameter(s):
  - _{year}_
  - _{category}_

`http://bootcamp.brogard.io:5051/ads/{year}/year/{category}/category`

>example:

[http://bootcamp.brogard.io:5051/ads/2015/year/Electronics/category](http://bootcamp.brogard.io:5051/ads/2015/year/Electronics/category)

----

#### returns average price by category for each year for a specific store
- parameter(s):
  - _{store}_

`http://bootcamp.brogard.io:5051/ads/summary/{store}/store`

>example:

[http://bootcamp.brogard.io:5051/ads/summary/KMART/store](http://bootcamp.brogard.io:5051/ads/summary/KMART/store)

----

#### returns list of all stores

`http://bootcamp.brogard.io:5051/stores`

>example:
>
[http://bootcamp.brogard.io:5051/years](http://bootcamp.brogard.io:5051/stores)