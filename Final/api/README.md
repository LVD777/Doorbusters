# API Docs

----

#### returns of list of stores

`http://bootcamp.brogard.io:5051/stores`
>example:
>
[http://bootcamp.brogard.io:5051/stores](http://bootcamp.brogard.io:5051/stores)


#### returns of list of stores for a specific year
- parameter(s):
  - _{year}_
 
`http://bootcamp.brogard.io:5051/stores/{year}/year`

>example:
>
[http://bootcamp.brogard.io:5051/stores/2017/year](http://bootcamp.brogard.io:5051/stores/2017/year)


----

#### returns of list of categories

[http://bootcamp.brogard.io:5051/categories](http://bootcamp.brogard.io:5051/categories)

`http://bootcamp.brogard.io:5051/categories`


#### returns categories for a specific year
- parameter(s):
  - _{year}_

`http://bootcamp.brogard.io:5051/categories/{year}/year`

>example:
>
[http://bootcamp.brogard.io:5051/categories/2015/year](http://bootcamp.brogard.io:5051/categories/2015/year)

----

#### returns list of years

`http://bootcamp.brogard.io:5051/years`

>example:
>
[http://bootcamp.brogard.io:5051/years](http://bootcamp.brogard.io:5051/years)

----

#### returns ads for a specific category and year
- parameter(s):
  - _{year}_
  - _{category}_

`http://bootcamp.brogard.io:5051/ads/{year}/year/{category}/category`

>example:

[http://bootcamp.brogard.io:5051/ads/2015/year/Electronics/category](http://bootcamp.brogard.io:5051/ads/2015/year/Electronics/category)

----

#### returns summary of ads

`http://bootcamp.brogard.io:5051/ads/summary`

>example:
>
[http://bootcamp.brogard.io:5051/ads/summary](http://bootcamp.brogard.io:5051/ads/summary)

#### returns average price by category for each year for a specific store
- parameter(s):
  - _{store}_

`http://bootcamp.brogard.io:5051/ads/summary/{store}/store`

>example:

[http://bootcamp.brogard.io:5051/ads/summary/KMART/store](http://bootcamp.brogard.io:5051/ads/summary/KMART/store)

#### return average price for each store and category for a specific year
- parameter(s):
  - _{year}_

`http://bootcamp.brogard.io:5051/ads/summary/{year}/year`

>example:
>
[http://bootcamp.brogard.io:5051/ads/summary/2017/year](http://bootcamp.brogard.io:5051/ads/summary/2017/year)

#### return ad details for each store for a specific year
- parameter(s):
  - _{year}_

`http://bootcamp.brogard.io:5051/ads/summary/detail/<parm_year>/year`

>example:
>
[http://bootcamp.brogard.io:5051/ads/summary/detail/2015/year](http://bootcamp.brogard.io:5051/ads/summary/detail/2015/year)

----

#### return lat, lng, count for a specific store
- parameter(s):
  - _{store}_
 
`http://bootcamp.brogard.io:5051/geo/stats/<parm_store>/store`

>example:
>
[http://bootcamp.brogard.io:5051/geo/stats/KMART/store](http://bootcamp.brogard.io:5051/geo/stats/KMART/store)

#### return lat, lng, count for a specific year
- parameter(s):
  - _{year}_
 
`http://bootcamp.brogard.io:5051/geo/stats/<parm_year>/year`

>example:
>
[http://bootcamp.brogard.io:5051/geo/stats/2014/year](http://bootcamp.brogard.io:5051/geo/stats/2014/year)

#### return lat, lng, count for a specific year and store
- parameter(s):
  - _{year}_
  - _{store}_
 
`http://bootcamp.brogard.io:5051/geo/stats/<parm_year>/year/<parm_store>/store`

>example:
>
[http://bootcamp.brogard.io:5051/geo/stats/2015/year/TARGET/store](http://bootcamp.brogard.io:5051/geo/stats/2015/year/TARGET/store)




