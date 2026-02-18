import pandas as pd
from datetime import datetime 
import geopandas as gpd
import numpy as np
from typing import Callable




def assign_date(dataset:gpd.GeoDataFrame):
    """
    Adding a 'Date_Added' column with that day's date

    Parameters:
        gdf (gpd.GeoDataFrame) : Input GeoDataFrame

    Returns:
        gdf (gpd.GeoDataFrame) 

    
    """
    dataset['Date_Added'] = datetime.today().date()
    dataset['Date_Added'] = dataset['Date_Added'].astype(str)  





def yield_process(column,current_unit):
    """
    Normalize the Yield column units to ton/ha
    allowed_units = 'centner/ha','ton/ha','quintal/ha','kilogram/ha'
    """
    allowed_units = {'centner/ha','ton/ha','quintal/ha','kilogram/ha'}
    if current_unit not in allowed_units:
        raise ValueError(f"Invalid unit '{current_unit}.' Allowed units are: {','.join(allowed_units)} ")
    
    if not isinstance(column, (pd.Series, np.ndarray, list)):
        raise TypeError("Input column must be a Pandas Series, NumPy array, or list of numbers")
    
    if not np.issubdtype(np.array(column).dtype,np.number):
        raise TypeError("Input column must contain numeric values only") 
    
    if current_unit == 'centner/ha':
        print(f"The yield units have been successfully changed from {current_unit} to ton/ha \n")
        return np.array(column) / 10
    if current_unit in {'ton/ha','quintal/ha'}:
        print(f"The yield units have been successfully changed from {current_unit} to ton/ha \n")
        return np.array(column)
    if current_unit == 'kilogram/ha':
        print(f"The yield units have been successfully changed from {current_unit} to ton/ha \n")
        return np.array(column) / 100

def build_season_id(row):
    """Build season_id for a single row."""
    geom_id = row.get("Geom_id")
    
    if pd.isna(row.get("Sow_Year")):
        est_year = row.get("Est_Sow_Year")
        
        if pd.isna(est_year):
            return None
        
        return f"{geom_id}-{int(est_year)}_EST"
    
    parts = [str(geom_id), str(int(row["Sow_Year"]))]
    
    if not pd.isna(row.get("Sow_Month")):
        parts.append(f"{int(row['Sow_Month']):02d}")
    
    if not pd.isna(row.get("Sow_Day")):
        parts.append(f"{int(row['Sow_Day']):02d}")
        
    return "-".join(parts)


def assign_season_id(gdf: gpd.GeoDataFrame):
    """Assign Season_id column to GeoDataFrame."""
    required = ["Geom_id","Sow_Year"]
    missing = [col for col in required if col not in gdf.columns]
    if missing:
        raise ValueError(f"Missing required columns for Season_id: {missing}")
    gdf["Season_id"] = gdf.apply(build_season_id, axis=1)
    return gdf

#def assign_season_id(gdf:gpd.GeoDataFrame):
#    """
#    Assigns the Season_id based on the Sow_Year, Est_Sow_Year and Geom_id 
#
#    Input: GeoDataframe
#
#    Returns: GeoDataFrame with a new column Season_id
#    
#    """
#    gdf["Season_id"] = np.where(
#        gdf["Sow_Year"].isnull(),
#        gdf["Geom_id"].astype(str) + "-" + gdf["Est_Sow_Year"].astype(str) + "_EST",
#        gdf["Geom_id"].astype(str) + "-" + gdf["Sow_Year"].astype(str) + gdf["Sow_Month"] + gdf["Sow_Day"]
#    )
#    return gdf


def to_datetime(string:str,date_format:str):

    """
    Converting date columns into datetime columns

    Parameters:
        string : Input string
    
    Returns:
        datetime object

    If non date values are encountered, converts it to NaT -> This part was changed recently to encounter any weird date types for better debugging
    This is also the reason of keeping using .apply instead of a vectorized operation (that would handle the none cases using errors="raise")
    
    """
    # If the input is None or null, return None without further processing
    if string is None or pd.isnull(string):
        return None
    
    # Convert string to datetime object
    return pd.to_datetime(string, format = date_format, errors='raise')

def convert_multiple_datetime(df:pd.DataFrame, dict_mapping:dict, func:Callable):
    """
    Helper function to perform multiple operations cleanly

    Input: 
    1. Dataframe on which the operations need to be done
    2. Dictionary with the old and new column names 
    3. Function that needs to be performed 
    
    """
    for col, info in dict_mapping.items():
        df[info["new_col"]] = df[col].apply(func, date_format = info["format"])
    return df

def date_to_dmy_cols(datetime_col:str,col_name:str):
    """
    Function to convert a datetime column to day, month and year columns

    Input: 
    1. Datetime column 
    2. Column name for the corresponding column

    Returns: 
    Dataframe: Day, month and year columns
    
    """
    day = datetime_col.dt.day.astype("Int64")
    month = datetime_col.dt.month.astype("Int64")
    year = datetime_col.dt.year.astype("Int64")
    return pd.DataFrame({
        f"{col_name}_Day": day,
        f"{col_name}_Month": month,
        f"{col_name}_Year": year
    })


def convert_multiple_dmy_cols(df:pd.DataFrame, dmy_cols_dict:dict, func:Callable):
    """
    Helper function to convert multiple datetime columns to separate day, month and year columns

    Input:
    1. Input dataframe
    2. Dictionary with the column names and the renamed column names
    3. Function that needs to be performed
    """
    df_total = pd.DataFrame(index=df.index)
    for col, prefix in dmy_cols_dict.items():

        new_cols = func(df[col], prefix)
        df_total = pd.concat([df_total, new_cols], axis=1)
    return df_total

def to_numeric(series:pd.Series):
    """
    Normalize decimal separators in a Series and convert to numeric.

    """
    if not isinstance(series, pd.Series):
        raise TypeError("Input must be a pandas Series")
    
    cleaned = series.apply(lambda x: str(x).replace(',', '.') if pd.notna(x) else x)
    return pd.to_numeric(cleaned, errors='raise')

def to_numeric_series(series:pd.Series, str_replace:str, str_target:str):
    """
    Normalize decimal separators in a Series and convert to numeric.

    """
    if not isinstance(series, pd.Series):
        raise TypeError("Input must be a pandas Series")
    
    cleaned = series.apply(lambda x: str(x).replace(str_replace, str_target) if pd.notna(x) else x)
    return pd.to_numeric(cleaned, errors='raise')


def to_numeric_multiple(df:pd.DataFrame, numeric_dict:dict):
    for col, info in numeric_dict.items():
       df[info["new_col"]] = to_numeric_series(
           series=df[col],
           str_replace=info["str_replace"],
           str_target=info["str_target"])
    return df
