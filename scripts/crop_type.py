import pandas as pd
import re
#from utils import crop_variations,crop_codes
import sys
sys.path.append('..')
import utils

#Mapping the crop types to the variations from the crop_variations dictionary 
#Trying to make it replicabele for other dictionaries, this might move to a different file based on how much it is used outside of crop type operations
#Updated the model to handle none values as well. since tillage can have none values.
def map_variations(variation:str, dict_variations:dict = None):
    if variation is None or pd.isna(variation):
        return None
    for crop, variations in dict_variations.items():
        if variation.lower() in variations:
            return crop
    return variation.title()

def map_variations_multiple(variation:str):
    if variation is None: 
        return None  
    crops = variation.split(',') 
    mapped_crops = []  
    
    for crop in crops:
        crop = crop.strip()  # Remove leading/trailing spaces
        for standard_crop, variations in utils.crop_variations.items():
            if crop.lower() in variations:
                mapped_crops.append(standard_crop)
                break
        else:
            mapped_crops.append(crop.capitalize())  
    return ', '.join(mapped_crops)  

#Assigning crop code based on the crop heirarchy decided(check documentation) from crop_codes dictionary 
def code_variations(croptype:str, intercrop:str):
    for crop, code in utils.crop_codes.items():
        if croptype == crop:
            if pd.isna(intercrop):
                return str(code)
            else:
                return 'I' + str(code)
    return 999
#Accomodating intercrops into a separate intercropped column 
def parse_crop_type(value, crop_variations, separators=r'[_,-]'):
    parts = re.split(separators, value.lower())  # split on _, -, or ,
    
    # Apply your mapping to each part
    mapped = [map_variations(part.strip()) for part in parts]
    
    first_crop = mapped[0]
    intercrops = ', '.join(mapped[1:]) if len(mapped) > 1 else None
    return pd.Series([first_crop, intercrops])
#Adding a new crop code that is not present in the existing crop_codes dictionary
def add_crop_code(crop,category,current_codes):
    base = category * 100
    existing = [code for code in current_codes if base < code < base + 100]
    new_code = max(existing, default=base) + 1 
    prefix = crop.split('_')[0]
    suffix = crop.split('_')[1] if '_' in crop else None
    if suffix and suffix in current_codes:
        new_code = current_codes[suffix]
    if prefix == 'Winter': 
        new_code = new_code * 10 + 1
    elif prefix == 'Summer':
        new_code = new_code * 10 + 2
    elif prefix == 'Silage':
        new_code = new_code * 10 + 3
    
    return new_code

#
def assign_crop_columns(crop_list:list,season_codes_dict:dict,variation_codes_dict:dict,crop_to_group_dict:dict):
    """
    Creates the Season, Variation and Group columns for the Crop table

    Parameters: 
    1. List of crops
    2. Dictionary of season codes 
    3. Dictionary of variation codes
    4. Dictionary of group codes

    Returns:
    Pandas series containing the Season, Variation, Crop and Group columns

    """

    season, variation, crop, group = None, None, None, None

    for item in crop_list:
        if item in season_codes_dict.keys():
            season = item
        elif item in variation_codes_dict.keys():
            variation = item
        elif item in crop_to_group_dict.keys():
            crop = item
            group = crop_to_group_dict[item]

    return pd.Series([group,season,variation,crop], index = ['Crop_Group','Crop_Season','Crop_Variation','Crop'])

def remove_null_ct(ct_column_name:str,dataset:pd.DataFrame):
    """
    Removes all the rows from the dataset with null crop type

    Parameters:
    1. Crop column name in the input dataframe
    2. Input dataframe

    Returns:
    DataFrame without rows with null crop type
    
    """
    no_ct_df = dataset[dataset[ct_column_name].isna()]
    dataset = dataset[dataset[ct_column_name].notna()]
    print('Number of null crop rows removed from the dataset: ', len(no_ct_df))
    return dataset