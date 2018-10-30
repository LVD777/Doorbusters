

```python
## Imports
# Dependencies and Setup
import pandas as pd
import numpy as np
import datetime
```


```python
# Data file locations
data_dir      = "data-black-friday"
src_dir       = "{}/src".format(data_dir)
report_dir    = "{}/report".format(data_dir)
clean_dir     = "{}/clean".format(data_dir)

# Raw data file(s)
csv_files = {"2011":"deals.20111124.csv",
             "2012":"deals.20121121.csv",
             "2013":"deals.20131127.csv",
             "2014":"deals.20141127.csv",
             "2015":"deals.20151126.csv",
             "2016":"deals.20161124.csv",
             "2017":"deals.20171123.csv",
             "store-names":"bfa.store.names.csv",
             "store-category":"bfa.store.category.csv",
             "sanitized":"bfa.csv",
             "san-2011":"bfa.2011.csv",
             "san-2012":"bfa.2012.csv",
             "san-2013":"bfa.2013.csv",
             "san-2014":"bfa.2014.csv",
             "san-2015":"bfa.2015.csv",
             "san-2016":"bfa.2016.csv",
             "san-2017":"bfa.2017.csv"}
```


```python
'''
## Functions
-------------------------------------------------
'''
def now():
    return str(datetime.datetime.now())

def path_source(filename):
    result = "{}/{}".format(src_dir, filename)
    return result

def path_clean(filename):
    result = "{}/{}".format(clean_dir, filename)
    return result

def path_report(filename):
    result = "{}/{}".format(report_dir, filename)
    return result
```

## read in the goods -- raw source data files


```python
df2011 = pd.read_csv(path_source(csv_files["2011"]), names=['Store','Category','Item','Price'])
df2012 = pd.read_csv(path_source(csv_files["2012"]))
df2013 = pd.read_csv(path_source(csv_files["2013"]))
df2014 = pd.read_csv(path_source(csv_files["2014"]))
df2015 = pd.read_csv(path_source(csv_files["2015"]))
df2016 = pd.read_csv(path_source(csv_files["2016"]))
df2017 = pd.read_csv(path_source(csv_files["2017"]))
```

## clean the data

- drop data that is not needed


```python
df2012.drop(columns=['Early Bird','Rebate'], inplace=True)
df2013.drop(columns=['Early Bird','Rebate'], inplace=True)
df2014.drop(columns=['Early Bird','Rebate','URL'], inplace=True)
df2015.drop(columns=['Early Bird','Rebate','URL'], inplace=True)
df2016.drop(columns=['URL'], inplace=True)
df2017.drop(columns=['Original or Current Price','URL'], inplace=True)
```


```python
df2017.rename(columns = {'Sale Price':'Price'}, inplace=True)
```


```python
df2011['SubCategory'] = '';
df2012['SubCategory'] = '';
```

- break apart into to category columns


```python
df2017['Category'], df2017['SubCategory'] = df2017['Category'].str.split(' >> ', 1).str
df2016['Category'], df2016['SubCategory'] = df2016['Category'].str.split(' >> ', 1).str
df2015['Category'], df2015['SubCategory'] = df2015['Category'].str.split(' >> ', 1).str
df2014['Category'], df2014['SubCategory'] = df2014['Category'].str.split(' >> ', 1).str
df2013['Category'], df2013['SubCategory'] = df2013['Category'].str.split(' >> ', 1).str
```


```python
df2013['Category'], df2013['SubCategory'] = df2013['Category'].str.split(' > ', 1).str
```

- remove $ from price; convert to number and in process return NaN for non-numeric entries


```python
df2017['Price'] = pd.to_numeric(df2017['Price'].replace('[\$,]', '', regex=True),  errors='coerce')
df2016['Price'] = pd.to_numeric(df2016['Price'].replace('[\$,]', '', regex=True),  errors='coerce')
df2015['Price'] = pd.to_numeric(df2015['Price'].replace('[\$,]', '', regex=True),  errors='coerce')
df2014['Price'] = pd.to_numeric(df2014['Price'].replace('[\$,]', '', regex=True),  errors='coerce')
df2013['Price'] = pd.to_numeric(df2013['Price'].replace('[\$,]', '', regex=True),  errors='coerce')
df2012['Price'] = pd.to_numeric(df2012['Price'].replace('[\$,]', '', regex=True),  errors='coerce')
df2011['Price'] = pd.to_numeric(df2011['Price'].replace('[\$,]', '', regex=True),  errors='coerce')
```

- drop NaN rows


```python
df2017 = df2017[df2017['Price'].notnull()]
df2016 = df2016[df2016['Price'].notnull()]
df2015 = df2015[df2015['Price'].notnull()]
df2014 = df2014[df2014['Price'].notnull()]
df2013 = df2013[df2013['Price'].notnull()]
df2012 = df2012[df2012['Price'].notnull()]
df2011 = df2011[df2011['Price'].notnull()]
```

- upper case the store name


```python
df2011['Store'] = df2011['Store'].str.upper()
df2012['Store'] = df2012['Store'].str.upper()
df2013['Store'] = df2013['Store'].str.upper()
df2014['Store'] = df2014['Store'].str.upper()
df2015['Store'] = df2015['Store'].str.upper()
df2016['Store'] = df2016['Store'].str.upper()
df2017['Store'] = df2017['Store'].str.upper()
```

- append year column


```python
df2011['Year'] = 2011
df2012['Year'] = 2012
df2013['Year'] = 2013
df2014['Year'] = 2014
df2015['Year'] = 2015
df2016['Year'] = 2016
df2017['Year'] = 2017
```

## prepare DataFreames for CSV output

- 'clean' dataframe for each year


```python
yr2011 = df2011[['Year', 'Store', 'Category', 'SubCategory', 'Item', 'Price']]
yr2012 = df2012[['Year', 'Store', 'Category', 'SubCategory', 'Item', 'Price']]
yr2013 = df2013[['Year', 'Store', 'Category', 'SubCategory', 'Item', 'Price']]
yr2014 = df2014[['Year', 'Store', 'Category', 'SubCategory', 'Item', 'Price']]
yr2015 = df2015[['Year', 'Store', 'Category', 'SubCategory', 'Item', 'Price']]
yr2016 = df2016[['Year', 'Store', 'Category', 'SubCategory', 'Item', 'Price']]
yr2017 = df2017[['Year', 'Store', 'Category', 'SubCategory', 'Item', 'Price']]
```

- package all the good in together


```python
sanitized_df = pd.DataFrame(pd.concat([yr2011, yr2012, yr2013, yr2014, yr2015, yr2016, yr2017]))
sanitized_df = sanitized_df.sort_values(['Year', 'Store']).reset_index(drop=True)
```

- get unique store names and categories


```python
store_Names_df = pd.DataFrame(pd.concat([df2011['Store'].drop_duplicates(),
                               df2012['Store'].drop_duplicates(),
                               df2013['Store'].drop_duplicates(),
                               df2014['Store'].drop_duplicates(),                              
                               df2015['Store'].drop_duplicates(),
                               df2016['Store'].drop_duplicates(),
                               df2017['Store'].drop_duplicates()]))

store_Names_df = store_Names_df.drop_duplicates()
store_Names_df = store_Names_df.rename(columns = {'Store':'name'}).sort_values('name').reset_index(drop=True)
```


```python
store_Category_df = pd.DataFrame(pd.concat([df2011['Category'].drop_duplicates(),
                               df2012['Category'].drop_duplicates(),
                               df2013['Category'].drop_duplicates(),
                               df2014['Category'].drop_duplicates(),                              
                               df2015['Category'].drop_duplicates(),
                               df2016['Category'].drop_duplicates(),
                               df2017['Category'].drop_duplicates()]))

store_Category_df = store_Category_df.drop_duplicates().sort_values('Category').reset_index(drop=True)
```

## write CSV files


```python
store_Names_df.to_csv(path_report(csv_files["store-names"]), index=False)
store_Category_df.to_csv(path_report(csv_files["store-category"]), index=False)
```


```python
yr2011.to_csv(path_clean(csv_files["san-2011"]), index=False)
yr2012.to_csv(path_clean(csv_files["san-2012"]), index=False)
yr2013.to_csv(path_clean(csv_files["san-2013"]), index=False)
yr2014.to_csv(path_clean(csv_files["san-2014"]), index=False)
yr2015.to_csv(path_clean(csv_files["san-2015"]), index=False)
yr2016.to_csv(path_clean(csv_files["san-2016"]), index=False)
yr2017.to_csv(path_clean(csv_files["san-2017"]), index=False)
```


```python
sanitized_df.to_csv(path_clean(csv_files["sanitized"]), index=False)
```
