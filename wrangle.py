import pandas as pd

#Used handle missing valus function from program material. Columns must have min of 60% non-null values and rows min of 75% non-null or be dropped.
def handle_missing_values(df, prop_required_column = .60, prop_required_row = .75):
    threshold = int(round(prop_required_column*len(df.index),0))
    df.dropna(axis=1, thresh=threshold, inplace=True)
    threshold = int(round(prop_required_row*len(df.columns),0))
    df.dropna(axis=0, thresh=threshold, inplace=True)
    return df

#Function to remove unneeded columns. It will be used in wrangle function.
def remove_columns(df, cols_to_remove):  
    df = df.drop(columns=cols_to_remove)
    return df




def wrangle_zillow(df):
    #Group by parcelid and transactiondate to finish filtering from Sql query.
    df = df[df.groupby('parcelid')['transactiondate'].transform('max') == df['transactiondate']]
    #Instead of filtering by unitcnt, filter using propertylanduse looking for single fam homes.
    df = df[df['propertylandusedesc'].isin(['Single Family Residential', 'Manufactured, Modular, Prefabricated Homes', 'Townhouse', 'Mobile Home ' ])]
    #Run handle missing values function
    df = handle_missing_values(df)
    #Change fips codes to county names
    df.loc[(df.fips == 6037.0),'fips']='Los Angeles County'
    df.loc[(df.fips == 6111.0),'fips']='Ventura County'
    df.loc[(df.fips == 6059.0),'fips']='Orange County'
    #Turn year built into a usable column
    df['age'] = 2020 - df['yearbuilt']
    #Reduce taxamount and value into a single column of tax percent
    df['tax_percentage'] = round(df['taxamount'] / df['taxvaluedollarcnt'],4)
    #Filter outliers
    df = df[df['bathroomcnt'] > 0]
    df = df[df['bedroomcnt'] > 0]
    df = df[df['bedroomcnt'] < 8]
    df = df[df['calculatedfinishedsquarefeet'] < 7000]
    #Remove unwanted columns including ids, redundant columns
    df = remove_columns(df, ['id','parcelid', 'roomcnt', 'propertylandusedesc','finishedsquarefeet12', 'regionidzip', 'heatingorsystemdesc', 'unitcnt','censustractandblock','calculatedbathnbr','fullbathcnt', 'regionidcity' , 'structuretaxvaluedollarcnt', 'landtaxvaluedollarcnt','propertycountylandusecode', 'propertylandusetypeid', 'regionidcounty' , 'assessmentyear', 'propertyzoningdesc','transactiondate','heatingorsystemtypeid', 'buildingqualitytypeid','yearbuilt', 'taxamount', 'taxvaluedollarcnt' ])
    #Convert categorical column to dummies
    return df



