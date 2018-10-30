#!/opt/anaconda3/bin/python

## Imports
import os, sqlalchemy, pymysql
import pandas as pd
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import MetaData, Table, Column, String, Integer
from flask import Flask, jsonify
from flask_jsonpify import jsonpify
from flask_sqlalchemy import SQLAlchemy

## FLASK init
app = Flask(__name__)

## Database (init)
pymysql.install_as_MySQLdb()

## Database (MySQL init)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:scyLLa!4dev@localhost/bfa"
db = SQLAlchemy(app)
Base = automap_base()

class tbl_bfa_geo_stats(Base):
    __table__ = Table('geo_stats', Base.metadata,
        Column('id', Integer, primary_key=True),
        Column('year', Integer),                      
        Column('store', String),
        Column('lat', String),
        Column('lng', String),                      
        Column('count', Integer),
            autoload=True, autoload_with=db.engine
        )

class tbl_bfa_store_counts(Base):
    __table__ = Table('store_counts', Base.metadata,
        Column('id', Integer, primary_key=True),
        Column('year', Integer),                      
        Column('store', String),
        Column('count', String),
            autoload=True, autoload_with=db.engine
        )

Base.prepare(db.engine, reflect=True)

## Database tables
tbl_bfa_ads = Base.classes.ads
tbl_bfa_geo = Base.classes.geo
tbl_bfa_year = Base.classes.year
tbl_bfa_category = Base.classes.category


'''
    /stores
    @return stores
'''
@app.route("/stores")
def get_stores():
    sql = db.session.query(tbl_bfa_ads.store).statement
    dfs = pd.read_sql_query(sql, db.session.bind)
    dfs = pd.DataFrame(dfs).drop_duplicates()
    dfs = dfs.rename(columns = {'store':'name'}).sort_values('name').reset_index(drop=True)
  
    return jsonify(list(dfs.iloc[:,0]))

'''
    /stores
    @return stores
'''
@app.route("/stores/<parm_year>/year")
def get_stores_parm_year(parm_year):
    sql = db.session.query(tbl_bfa_store_counts.store).filter(tbl_bfa_store_counts.year == parm_year).statement
    dfs = pd.read_sql_query(sql, db.session.bind)
  
    return jsonify(list(dfs.iloc[:,0]))

'''
    /categories
    @return categories
'''
@app.route("/categories")
def get_categories():
    sql = db.session.query(tbl_bfa_year.year, tbl_bfa_category.name) \
            .filter(tbl_bfa_year.id == tbl_bfa_category.year_id) \
            .statement
    dfs = pd.read_sql_query(sql, db.session.bind)
    
    df_dict = { "year"       : 2011,
                "categories" : list(dfs[dfs['year'] == 2011].iloc[:,1])
              },{
                "year"       : 2012,
                "categories" : list(dfs[dfs['year'] == 2012].iloc[:,1])
              },{
                "year"       : 2013,
                "categories" : list(dfs[dfs['year'] == 2013].iloc[:,1])       
              },{        
                "year"       : 2014,
                "categories" : list(dfs[dfs['year'] == 2014].iloc[:,1])       
              },{        
                "year"       : 2015,
                "categories" : list(dfs[dfs['year'] == 2015].iloc[:,1])       
              },{        
                "year"       : 2016,
                "categories" : list(dfs[dfs['year'] == 2016].iloc[:,1])       
              },{        
                "year"       : 2017,
                "categories" : list(dfs[dfs['year'] == 2017].iloc[:,1])       
              }       
                
    return jsonify(df_dict)

'''
    /years
    @return years
'''
@app.route("/years")
def get_years():
    sql = db.session.query(tbl_bfa_year).statement
    dfs = pd.read_sql_query(sql, db.session.bind)
  
    return jsonify(list(dfs.iloc[:,1]))

'''
    /categories/<parm_year>/year
    @return categories
'''
@app.route("/categories/<parm_year>/year")
def get_categories_by_year(parm_year):
    sql = db.session.query(tbl_bfa_category) \
            .filter(tbl_bfa_year.id == tbl_bfa_category.year_id) \
            .filter(tbl_bfa_year.year == parm_year) \
            .statement
    dfs = pd.read_sql_query(sql, db.session.bind)
                
    return jsonify(list(dfs.iloc[:,2]))

'''
    /ads/<parm_year>/year/<parm_category>/category
    @return stores;items;price
'''
@app.route("/ads/<parm_year>/year/<parm_category>/category")
def get_ads_by_year_parm_category(parm_year, parm_category):
    sql = db.session.query(tbl_bfa_ads.store, tbl_bfa_ads.item, tbl_bfa_ads.price) \
                    .filter(tbl_bfa_ads.category == parm_category) \
                    .filter(tbl_bfa_ads.year == parm_year) \
                    .statement
    dfs = pd.read_sql_query(sql, db.session.bind)
    
    count_df  = pd.DataFrame(dfs.groupby(['store']).count())
    median_df = pd.DataFrame(dfs.groupby(['store']).median()['price'].round(2))
    mean_df   = pd.DataFrame(dfs.groupby(['store']).mean()['price'].round(2))
    min_df    = pd.DataFrame(dfs.groupby(['store']).min()['price'].round(2))
    max_df    = pd.DataFrame(dfs.groupby(['store']).max()['price'].round(2))
    
    df_dict = {
        "year": parm_year,
        "category": parm_category,
        "plot" : {
                "stores": dfs.store.values.tolist(),
                "items": dfs.item.values.tolist(),
                "prices": dfs.price.values.tolist()        
                },
        "stats" : {
             "count"  : { "stores" : count_df.index.values.tolist(),
                          "counts" : count_df.item.values.tolist() 
                        },
             "median" : { "stores" : median_df.index.values.tolist(),
                          "prices" : median_df.price.values.tolist() 
                        },      
             "mean"   : { "stores" : mean_df.index.values.tolist(),
                          "prices" : mean_df.price.values.tolist() 
                        },
             "min"    : { "stores" : min_df.index.values.tolist(),
                          "prices" : min_df.price.values.tolist() 
                        },        
             "max"    : { "stores" : max_df.index.values.tolist(),
                          "prices" : max_df.price.values.tolist() 
                        }
                }
        }    

    return jsonify(df_dict)

'''
    /ads/summary/<parm_store>/store
    @return average price by category for store for each year
'''
@app.route("/ads/summary/<parm_store>/store")
def get_ads_summary_parm_store(parm_store):
    sql = db.session.query(tbl_bfa_ads.year, tbl_bfa_ads.category, tbl_bfa_ads.price).filter(tbl_bfa_ads.store == parm_store).statement
    dfs = pd.read_sql_query(sql, db.session.bind)
    
    mean_df = pd.DataFrame(dfs.groupby(['year', 'category']).mean()['price'].round(2))
    mean_df = mean_df.unstack(level=0)
    mean_df.columns = mean_df.columns.get_level_values(level=1)
    mdf = pd.DataFrame(mean_df).replace({np.nan:0})
    mdsf = mdf.to_dict('split')
  
    df_dict = { 
                "category" : mdsf['index'],
                "price"    : mdsf['data']
              }
  
    return jsonify(df_dict)

'''
    /ads/summary/<parm_year>/year
    @return average price for each store and category for a specific year
'''
@app.route("/ads/summary/<parm_year>/year")
def get_ads_summary_parm_year(parm_year):
    sql = db.session.query(tbl_bfa_ads.store, tbl_bfa_ads.category, tbl_bfa_ads.price).filter(tbl_bfa_ads.year == parm_year).statement
    dfs = pd.read_sql_query(sql, db.session.bind)
    
    mean_df = pd.DataFrame(dfs.groupby(['store', 'category']).mean()['price'].round(2)).reset_index()
    pvt_cnt_df = mean_df.pivot(index='store',columns='category',values='price')
    mdf = pd.DataFrame(pvt_cnt_df).replace({np.nan:0}).reset_index()
    
    df_arr = [mdf.to_dict('index')]
    
    return jsonify(df_arr)

'''
    /ads/summary/detail/<parm_year>/year
    @return average price for each store and category for a specific year
'''
@app.route("/ads/summary/detail/<parm_year>/year")
def get_ads_summary_detail_parm_year(parm_year):
    sql = db.session.query(tbl_bfa_ads.store, tbl_bfa_ads.category, tbl_bfa_ads.price).filter(tbl_bfa_ads.year == parm_year).statement
    dfs = pd.read_sql_query(sql, db.session.bind)
    
    count_df  = pd.DataFrame(dfs.groupby(['store']).count())
    median_df = pd.DataFrame(dfs.groupby(['store']).median()['price'].round(2))
    mean_df   = pd.DataFrame(dfs.groupby(['store']).mean()['price'].round(2))
    min_df    = pd.DataFrame(dfs.groupby(['store']).min()['price'].round(2))
    max_df    = pd.DataFrame(dfs.groupby(['store']).max()['price'].round(2))
    
    count = count_df.to_dict('dict')
    median = median_df.to_dict('dict')
    mean   = mean_df.to_dict('dict')
    mmin = min_df.to_dict('dict')
    mmax = max_df.to_dict('dict')
    
    dfs_arr = [dfs.to_dict('index')]
    
    df_dict = {
        "stores" : count_df.index.values.tolist(),
        "count"  : count['category'],
        "median" : median['price'],
        "mean"   : mean['price'],
        "min"    : mmin['price'],
        "max"    : mmax['price'],
        "plot"   : dfs.to_dict('index')
    }
    
    return jsonify(df_dict)

'''
    /ads/summary
    @return
'''
@app.route("/ads/summary")
def get_ads_summary():
    df_list = []
    
    sql = db.session.query(tbl_bfa_ads.store, tbl_bfa_ads.category, tbl_bfa_ads.item, tbl_bfa_ads.price).filter(tbl_bfa_ads.year == 2011).statement
    dfs = pd.read_sql_query(sql, db.session.bind)

    y2011 = pd.DataFrame(dfs.groupby(['store']).describe().round(2)).reset_index()
    y2011.columns.set_levels(['2011','store'],level=0,inplace=True)
    y2011.columns = ["_".join(x) for x in y2011.columns]
    y2011.insert(0, 'year', '2011')
    y2011.index.names = ['2011_ndx']
    y2011.reset_index(inplace=True)
    
    sql = db.session.query(tbl_bfa_ads.store, tbl_bfa_ads.category, tbl_bfa_ads.item, tbl_bfa_ads.price).filter(tbl_bfa_ads.year == 2012).statement
    dfs = pd.read_sql_query(sql, db.session.bind)
  
    y2012 = pd.DataFrame(dfs.groupby(['store']).describe().round(2)).reset_index()
    y2012.columns.set_levels(['2012','store'],level=0,inplace=True)
    y2012.columns = ["_".join(x) for x in y2012.columns]    
    y2012.insert(0, 'year', '2012')
    y2012.index.names = ['2012_ndx']
    y2012.reset_index(inplace=True)
    
    sql = db.session.query(tbl_bfa_ads.store, tbl_bfa_ads.category, tbl_bfa_ads.item, tbl_bfa_ads.price).filter(tbl_bfa_ads.year == 2013).statement
    dfs = pd.read_sql_query(sql, db.session.bind)
  
    y2013 = pd.DataFrame(dfs.groupby(['store']).describe().round(2)).reset_index()
    y2013.columns.set_levels(['2013','store'],level=0,inplace=True)
    y2013.columns = ["_".join(x) for x in y2013.columns]     
    y2013.insert(0, 'year', '2013')
    y2013.index.names = ['2013_ndx']
    y2013.reset_index(inplace=True)
    
    sql = db.session.query(tbl_bfa_ads.store, tbl_bfa_ads.category, tbl_bfa_ads.item, tbl_bfa_ads.price).filter(tbl_bfa_ads.year == 2014).statement
    dfs = pd.read_sql_query(sql, db.session.bind)
  
    y2014 = pd.DataFrame(dfs.groupby(['store']).describe().round(2)).reset_index()
    y2014.columns.set_levels(['2014','store'],level=0,inplace=True)
    y2014.columns = ["_".join(x) for x in y2014.columns]       
    y2014.insert(0, 'year', '2014')
    y2014.index.names = ['2014_ndx']
    y2014.reset_index(inplace=True)
    
    sql = db.session.query(tbl_bfa_ads.store, tbl_bfa_ads.category, tbl_bfa_ads.item, tbl_bfa_ads.price).filter(tbl_bfa_ads.year == 2015).statement
    dfs = pd.read_sql_query(sql, db.session.bind)
  
    y2015 = pd.DataFrame(dfs.groupby(['store']).describe().round(2)).reset_index()
    y2015.columns.set_levels(['2015','store'],level=0,inplace=True)
    y2015.columns = ["_".join(x) for x in y2015.columns]       
    y2015.insert(0, 'year', '2015')
    y2015.index.names = ['2015_ndx']
    y2015.reset_index(inplace=True)
    
    sql = db.session.query(tbl_bfa_ads.store, tbl_bfa_ads.category, tbl_bfa_ads.item, tbl_bfa_ads.price).filter(tbl_bfa_ads.year == 2016).statement
    dfs = pd.read_sql_query(sql, db.session.bind)
  
    y2016 = pd.DataFrame(dfs.groupby(['store']).describe().round(2)).reset_index()
    y2016.columns.set_levels(['2016','store'],level=0,inplace=True)
    y2016.columns = ["_".join(x) for x in y2016.columns] 
    y2016.insert(0, 'year', '2016')
    y2016.index.names = ['2016_ndx']
    y2016.reset_index(inplace=True)
 
    sql = db.session.query(tbl_bfa_ads.store, tbl_bfa_ads.category, tbl_bfa_ads.item, tbl_bfa_ads.price).filter(tbl_bfa_ads.year == 2017).statement
    dfs = pd.read_sql_query(sql, db.session.bind)
  
    y2017 = pd.DataFrame(dfs.groupby(['store']).describe().round(2)).reset_index()
    y2017.columns.set_levels(['2017','store'],level=0,inplace=True)
    y2017.columns = ["_".join(x) for x in y2017.columns]
    y2017.insert(0, 'year', '2017')
    y2017.index.names = ['2017_ndx']
    y2017.reset_index(inplace=True)    
    
    df = pd.DataFrame(pd.concat([y2011, y2012, y2013, y2014, y2015, y2016, y2017], sort=False)).replace({np.nan:0}).reset_index()
    df.columns = df.columns.str.replace("%", "per")
    df = df.rename(columns = {'store_':'store'})
    
    df_dict = df.to_dict('index')
    
    for i in range(len(df_dict)):
        df_list.append(df_dict[i])
    
    return jsonify(df_list)

'''
    /geo/stats/<parm_store>/store
    @return lat, lng, count for a specific store
'''
@app.route("/geo/stats/<parm_store>/store")
def get_geo_stats_parm_store(parm_store):
    sql = db.session.query(tbl_bfa_geo_stats.lat, tbl_bfa_geo_stats.lng, tbl_bfa_geo_stats.count) \
                    .filter(tbl_bfa_geo_stats.store == parm_store) \
                    .statement    
    dfs = pd.read_sql_query(sql, db.session.bind)
    dfs = dfs.to_dict('split')
    
    return jsonify(dfs['data'])

'''
    /geo/stats/<parm_year>/year
    @return lat, lng, count for a specific year
'''
@app.route("/geo/stats/<parm_year>/year")
def get_geo_stats_parm_year(parm_year):
    sql = db.session.query(tbl_bfa_geo_stats.lat, tbl_bfa_geo_stats.lng, tbl_bfa_geo_stats.count) \
                    .filter(tbl_bfa_geo_stats.year == parm_year) \
                    .statement
    dfs = pd.read_sql_query(sql, db.session.bind)
    dfs = dfs.to_dict('split')
    
    return jsonify(dfs['data'])

'''
    /geo/stats/<parm_year>/year/<parm_store>/store
    @return lat, lng, count for a specific year and store
'''
@app.route("/geo/stats/<parm_year>/year/<parm_store>/store")
def get_geo_stats_parm_year_parm_store(parm_year, parm_store):
    sql = db.session.query(tbl_bfa_geo_stats.lat, tbl_bfa_geo_stats.lng, tbl_bfa_geo_stats.count) \
                    .filter(tbl_bfa_geo_stats.year == parm_year) \
                    .filter(tbl_bfa_geo_stats.store == parm_store) \
                    .statement    
    dfs = pd.read_sql_query(sql, db.session.bind)
    dfs = dfs.to_dict('split')
    
    return jsonify(dfs['data'])



### ---------------------------------------------------------------------- ###



## Main functionality
if __name__ == "__main__":
    app.run(debug=True)

