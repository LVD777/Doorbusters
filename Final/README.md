# Project - Presentation

> [http://doorbusters.bootcamp.brogard.io/](http://doorbusters.bootcamp.brogard.io/)


## Requirements Check

1. Your visualization must include a Python Flask powered RESTful API, HTML/CSS, JavaScript, and at least one database

	> ### Python Flask API, MySQL

2. Your project should fall into one of the below four tracks: 
	 - A custom "creative" D3.js project (i.e. non-standard graph or chart)

	 - A combination of Web Scraping and Leaflet or Plotly
 		> Leaflet, Plotly

	 - A dashboard page with multiple charts all updating from the same data
 		> main entry page: **pie chart**, **bubble chart**

	 - A "thick" server that performs multiple manipulations on data in a database prior to visualization
 		> SQL views 

3. Your project should include at least one JS library that we did not cover.

	> ### Underscore.js
	> [https://underscorejs.org/](https://underscorejs.org/)

4. Your project must be powered by a dataset with at least 100 records.
	
	> bfa.ads : 142,840
	
	> bfa.geo :  63,417
	
5. Your project must include some level of user-driven interaction
	> [http://doorbusters.bootcamp.brogard.io/Statistical-Analysis/](http://doorbusters.bootcamp.brogard.io/Statistical-Analysis/)
	> [http://doorbusters.bootcamp.brogard.io/Stores-Locations/](http://doorbusters.bootcamp.brogard.io/Stores-Locations/)	

6. Your final visualization should ideally include at least three views
	> [http://doorbusters.bootcamp.brogard.io/](http://doorbusters.bootcamp.brogard.io/) 	
	> [http://doorbusters.bootcamp.brogard.io/Statistical-Analysis/](http://doorbusters.bootcamp.brogard.io/Statistical-Analysis/)

	> [http://doorbusters.bootcamp.brogard.io/Metrics/average-price/](http://doorbusters.bootcamp.brogard.io/Metrics/average-price/)
	
	> [http://doorbusters.bootcamp.brogard.io/Metrics/product-count/](http://doorbusters.bootcamp.brogard.io/Metrics/product-count/)

	> [http://doorbusters.bootcamp.brogard.io/Stores-Locations/](http://doorbusters.bootcamp.brogard.io/Stores-Locations/)

---

## Repo Layout


```
├── api
├── htdocs-doorbusters
└── scripts
```

- api
	- Python Flask API
	- SQLAlchemy
    - MySQL Connection
    - SQL views
- htdocs-doorbusters
	- web root folder
	- HTML, CSS, JS
- scripts
	- mapster
		- Python, Pandas
		- geo location lookup
		- Google Places API
	- munger
		- Python, Pandas
		- data cleaning
