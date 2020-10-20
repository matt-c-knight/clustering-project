from env import host, user, password

import pandas as pd
import numpy as np
import os

def get_connection(db, user=user, host=host, password=password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'


def new_zillow_data():
    
    sql_query = "SELECT properties_2017.*, predictions_2017.logerror, predictions_2017.transactiondate, airconditioningdesc, architecturalstyledesc, buildingclassdesc, heatingorsystemdesc, propertylandusedesc, storydesc, typeconstructiondesc FROM properties_2017 LEFT JOIN predictions_2017 using(parcelid) LEFT JOIN architecturalstyletype using(architecturalstyletypeid) LEFT JOIN buildingclasstype using(buildingclasstypeid) LEFT JOIN heatingorsystemtype using(heatingorsystemtypeid) LEFT JOIN propertylandusetype using(propertylandusetypeid) LEFT JOIN storytype using(storytypeid) LEFT JOIN typeconstructiontype using(typeconstructiontypeid) LEFT JOIN airconditioningtype using(airconditioningtypeid) WHERE transactiondate LIKE '2017%%' and latitude IS NOT NULL and longitude is not null"
    df = pd.read_sql(sql_query, get_connection('zillow'))
    df.to_csv('new_zillow_df.csv')
    return df

def get_zillow_data(cached=False):
   
    if cached or os.path.isfile('new_zillow_df.csv') == False:
        df = new_zillow_data()
    else:
        df = pd.read_csv('new_zillow_df.csv', index_col=0)
    return df