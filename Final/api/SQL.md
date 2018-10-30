# SQL Views

#### count of each store by year

```
CREATE VIEW store_counts AS
SELECT
    UUID()      AS `id`,
    a.year,
    a.store,
    count(a.id) AS `count`
FROM
    ads a
GROUP BY a.year, a.store
```

#### geo data for each store with counts

```
CREATE VIEW geo_stats AS
SELECT
    UUID()                AS `id`,
    g.store               AS `store`,
    g.google_location_lat AS `lat`,
    g.google_location_lng AS `lng`,
    sc.year,
    sc.count
FROM
    geo g, 
    store_counts sc
WHERE g.store = sc.store
ORDER BY
    g.store
```


