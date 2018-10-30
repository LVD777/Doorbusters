#!/opt/anaconda3/bin/python

## Imports
# pip install flask_jsonpify
import os, sqlalchemy, pymysql
import pandas as pd
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

## FLASK init
app = Flask(__name__)

## Database (init)
pymysql.install_as_MySQLdb()

## Database (MySQL init)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:scyLLa!4dev@localhost/bfa"
db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)

tbl_bfa_ads = Base.classes.ads
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
def get_categories(parm_year):
    sql = db.session.query(tbl_bfa_category)                     \
            .filter(tbl_bfa_year.id == tbl_bfa_category.year_id) \
            .filter(tbl_bfa_year.year == parm_year)              \
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
                    .filter(tbl_bfa_ads.category == parm_category)                 \
                    .filter(tbl_bfa_ads.year == parm_year)                         \
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
    sql = db.session.query(tbl_bfa_ads.year, tbl_bfa_ads.category, tbl_bfa_ads.price) \
            .filter(tbl_bfa_ads.store == parm_store)                                  \
            .statement
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


### ---------------------------------------------------------------------- ###



## Main functionality
if __name__ == "__main__":
    app.run(debug=True)
