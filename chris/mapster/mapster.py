#!/opt/anaconda3/bin/python

## Imports
# Dependencies and Setup
import pandas as pd
import numpy as np
import datetime, json, requests, time, csv
from pandas.io.json import json_normalize

# Import logging
import logging, LOGS
from configparser import ConfigParser

## Module Constants
api_key = "AIzaSyBTygt0iTuAHmp5A-BYjE_byAROQ_E5y0M"
google_api_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={}+in+{}&key=AIzaSyBTygt0iTuAHmp5A-BYjE_byAROQ_E5y0M"

states = ["AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
stores = ["ABT-ELECTRONICS", "AC-MOORE", "ACADEMY-SPORTS", "ACE-HARDWARE", "ACME-TOOLS", "ADORAMA", "AEROPOSTALE", "AMAZON", "ANNAS-LINENS", "APPLE-STORE", "ASHLEY-FURNITURE", "AT-HOME", "BADCOCK", "BARNES-NOBLE", "BASS-PRO-SHOPS", "BATH-AND-BODY-WORKS", "BEALLS", "BEALLS-TEXAS", "BED-BATH-AND-BEYOND", "BELK", "BEST-BUY", "BIG-5-SPORTING-GOODS", "BIG-LOTS", "BJS-WHOLESALE", "BONTON", "BOSCOVS", "BOSE", "BUILD-A-BEAR", "BURKES-OUTLET", "BURLINGTON-COAT-FACTORY", "CABELAS", "CALLAWAY-APPAREL", "CAMPMOR", "CARTERS", "CHRISTMAS-TREE-SHOPS", "CHRISTOPHER-AND-BANKS", "COSTCO", "CRAFT-WAREHOUSE", "CUBAVERA", "CVS", "DELL", "DICKS-SPORTING-GOODS", "DISNEY-STORE", "DOLLAR-GENERAL", "DSW", "DUNHAMS-SPORTS", "EXPRESS", "FAMILY-DOLLAR", "FARM-AND-FLEET", "FARM-HOME-SUPPLY", "FIELD-STREAM", "FINISH-LINE-ONLINE", "FIVE-BELOW", "FREDMEYER", "FREDS", "FRYS-ELECTRONICS", "GAMESTOP", "GANDER-MOUNTAIN", "GOLF-GALAXY", "GORDMANS", "GROUPON", "GUITAR-CENTER", "HALF-PRICE-BOOKS", "HANCOCK-FABRICS", "HARBOR-FREIGHT", "HARMAN-KARDON", "HASTINGS", "HAVERTYS", "HEB", "HEB-PLUS", "HHGREGG", "HOME-DEPOT", "HP", "IKEA", "JCPENNEY", "JETCOM", "JOANN-FABRICS", "JOS-A-BANK", "JUST-CABINETS", "KINGSTON", "KMART", "KOHLS", "LA-Z-BOY", "LANDS-END", "LENOVO", "LIVING-SOCIAL", "LIVING-SPACES", "LORD-AND-TAYLOR", "LOWES", "MACMALL", "MACYS", "MC-SPORTS", "MEIJER", "MENARDS", "MICHAELS", "MICRO-CENTER", "MICROSOFT-STORE", "MILLS-FLEET-FARM", "MODELLS", "MONOPRICE", "MUSIC-AND-ARTS", "MUSIC-ARTS", "MUSICIANS-FRIEND", "NIKON", "NORTHERN-TOOL", "NYANDCOMPANY", "OCEAN-STATE-JOB-LOT", "OFF-BROADWAY-SHOES", "OFFICE-DEPOT", "OFFICE-MAX", "OLD-NAVY", "OLD-TIME-POTTERY", "OLYMPIA-SPORTS", "ORIGINAL-PENGUIN", "ORIGINS", "OVERSTOCK", "PACSUN", "PANASONIC", "PAYLESS-SHOES", "PC-RICHARD-SON", "PEPBOYS", "PERRY-ELLIS", "PET-SMART", "PET-SUPPLIES-PLUS", "PETCO", "PIER-1", "QUILL", "RACK-ROOM-SHOES", "RADIOSHACK", "RAKUTEN", "RAYMOUR-FLANIGAN", "REEDS-JEWELERS", "REI", "RITE-AID", "RURAL-KING", "SAM-ASH", "SAMS-CLUB", "SAMSUNG", "SEARS", "SEARS-OUTLET", "SEPHORA", "SHOE-CARNIVAL", "SHOPKO", "SIERRA-TRADING-POST", "SIGMA-BEAUTY", "SONY-STORE", "SPORTS-AUTHORITY", "SPORTSMANS-WAREHOUSE", "SPRINT", "STAGE", "STAPLES", "STEIN-MART", "TARGET", "TARGET-ONLINE-BLACK-FRIDAY", "THE-BODY-SHOP", "THINGS-REMEMBERED", "THINK-GEEK", "TIGER-DIRECT", "TILLYS", "TMOBILE", "TOYS-R-US", "TRACTOR-SUPPLY", "TRUE-VALUE", "ULTA", "US-CELLULAR", "US-MATTRESS", "VALUE-CITY", "VENUM", "VERIZON", "VICTORIAS-SECRET", "WALGREENS", "WALMART", "WEST-MARINE", "WOMAN-WITHIN", "WOODCRAFT", "WORLD-MARKET", "YANKEE-CANDLE", "ZALES"]

t_states = ["AL","AK","AZ","AR","CA"]
t_stores = ["ABT-ELECTRONICS", "AC-MOORE", "ACADEMY-SPORTS", "ACE-HARDWARE"]

sam_states = ["MO","IL"]
sam_stores = ["BEST-BUY","TARGET","ACE-HARDWARE"]

'''
## Functions
-------------------------------------------------
'''
def now():
    return str(datetime.datetime.now())

def current_date_timestamp():
    return time.strftime('%Y-%m-%d-%H.%M.%S')

def get_geo(state, store):
    url = google_api_url.format(store, state)
    LOGGER.info('Calling Google API: {}'.format(url))
    
    resp = requests.get(url).json()
    result = json_normalize(resp['results'])
    
    return result


'''
## Main
-------------------------------------------------
'''
def main():
    
    csv_file = "bfa.stores.geo-loc.{}.csv".format(current_date_timestamp())
    
    LOGGER.info('Mapster: START ##########################')
    
    summary_df = pd.DataFrame()
    
    lstates = states   
    lstores = stores
    
    # loop thru list of stores
    for store in lstores:
        LOGGER.info('Getting lat(s)/log(s) for : {}'.format(store))
        for state in lstates:
            LOGGER.info('Feteching geo data [state]: {}'.format(state))
            
            geo_result = get_geo(state, store)
            df = pd.DataFrame(geo_result)
            LOGGER.info('Result DataFrame length   : {}'.format(len(df)))
            
            df = pd.DataFrame(geo_result)
            
            if len(df) > 0:
                geo_df = pd.DataFrame(df[['place_id', 'name', 'formatted_address', 'geometry.location.lat', 'geometry.location.lng']])
                LOGGER.info('Geo data DataFrame shape  : {}'.format(df.shape))
            
                summary_df = pd.concat([summary_df, geo_df])
                LOGGER.info('Summary data frame shape  : {}'.format(summary_df.shape))
            pass
        
        pass
    
    LOGGER.info('Summary geo DataFrame {}'.format(summary_df.info()))
    
    LOGGER.info('Writing CSV file')
    summary_df.to_csv(csv_file, index=False, quoting=csv.QUOTE_ALL)
    
    LOGGER.info('Mapster: END ##########################')
    pass

if __name__ == "__main__":
    # Execute logging functionality
    log_conf = "conf/logger.conf"
    
    LOGGER = logging.getLogger(__name__)
    LOGS.init_logging(log_conf)    

    # Execute Main
    main()