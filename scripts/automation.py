import geopandas as gpd
import pandas as pd
from pathlib import Path
from typing import Union, List, Optional, Tuple
import scripts
import utils
import ipywidgets as widgets
from IPython.display import display, clear_output
import pprint

def read_ground_data(
    file_paths: Union[str, List[str]], 
    join_key: Union[str, Tuple[str, str], None] = None, 
    lat_lon_cols: Optional[tuple] = None
) -> gpd.GeoDataFrame:
    
    # ... [File Loading Logic remains exactly the same] ...
    # (Assuming we have now loaded 'gdf' and 'df')

    # 1. Normalize Input to a list of Path objects
    if isinstance(file_paths, str):
        files = [Path(file_paths)]
    else:
        files = [Path(f) for f in file_paths]

    geo_exts = {'.shp', '.geojson', '.gpkg', '.parquet', '.fgb'}
    table_exts = {'.csv', '.xlsx', '.xls', '.txt'}

    geo_file, attr_file = None, None

    for f in files:
        if not f.exists(): raise FileNotFoundError(f"File not found: {f}")
        if f.suffix.lower() in geo_exts: geo_file = f
        elif f.suffix.lower() in table_exts: attr_file = f
    
    if len(files) == 1 and not geo_file and not attr_file: geo_file = files[0]

    gdf, df = None, None

    # Load Geometry
    if geo_file:
        try:
            gdf = gpd.read_parquet(geo_file) if geo_file.suffix == '.parquet' else gpd.read_file(geo_file)
        except Exception as e: raise ValueError(f"Error reading geometry: {e}")

    # Load Attributes
    if attr_file:
        try:
            print(f"\n--- DEBUGGING EXCEL LOAD: {attr_file.name} ---")
            
            if attr_file.suffix in ['.xlsx', '.xls']:
                # 1. Read the file (defaults to first sheet)
                df = pd.read_excel(attr_file)
                
                # DIAGNOSTIC: Print what we found
                print(f"Columns detected: {list(df.columns)}")
                print(f"Row count: {len(df)}")
                print(f"First 2 rows:\n{df.head(2)}")
                
                # CHECK: Does it look like a valid table?
                # If the headers look like "Unnamed: 1", the header row is wrong.
                if "Unnamed: 0" in df.columns or "Unnamed: 1" in df.columns:
                    print("WARNING: 'Unnamed' columns detected. Your header might be on a lower row.")
                    # Optional: Try to auto-fix by grabbing the next valid row (Advanced)
            
            elif attr_file.suffix == '.csv':
                df = pd.read_csv(attr_file)
            elif attr_file.suffix == '.txt': 
                df = pd.read_csv(attr_file, sep='\t')
                
        except Exception as e:
            raise ValueError(f"Error reading attributes: {e}")

    # ==========================================
    # MERGE LOGIC WITH TYPE FIX
    # ==========================================
    if gdf is not None and df is not None:
        
        # 1. Determine the Left (Geo) and Right (Attr) keys
        left_key, right_key = None, None

        if isinstance(join_key, (tuple, list)) and len(join_key) == 2:
            left_key, right_key = join_key
        elif isinstance(join_key, str):
            left_key, right_key = join_key, join_key
        else:
            # Auto-detect
            common_cols = set(gdf.columns) & set(df.columns)
            common_cols.discard('geometry')
            if len(common_cols) == 1:
                k = list(common_cols)[0]
                left_key, right_key = k, k
            else:
                raise ValueError("Could not auto-detect join keys. Please specify.")

        # 2. VALIDATION
        if left_key not in gdf.columns: raise ValueError(f"Key '{left_key}' missing in Geometry file.")
        if right_key not in df.columns: raise ValueError(f"Key '{right_key}' missing in Attribute file.")

        # 3. TYPE HARMONIZATION (ROBUST FIX)
        print(f"Sanitizing keys: Casting '{left_key}' and '{right_key}'...")
        #Had to change it to this aggressive typcasting to get close to a standard method for getting equal keys for merging
        def clean_key_column(series):
            """
            Aggressively normalizes keys by trying to convert to integer first.
            Pipeline: Raw Value -> Float -> Int -> String
            Example: "123.0" -> 123.0 -> 123 -> "123"
            """
            try:
                # 1. Force to numeric (coerces errors to NaN)
                #    This handles '123', '123.0', '123.00', ' 123 '
                s_numeric = pd.to_numeric(series, errors='coerce')
                
                # 2. Check if we have valid numbers
                #    (If the whole column is "District A", this logic is skipped)
                if s_numeric.notna().sum() > 0:
                    # Fill NaNs with a dummy to allow Int casting, then cast to Int
                    # This chops off the decimal: 123.0 -> 123
                    s_int = s_numeric.fillna(-9999).astype(int).astype(str)
                    
                    # Restore NaNs
                    return s_int.replace('-9999', 'nan')
                else:
                    # Fallback for purely text columns
                    return series.astype(str).str.strip()
            except:
                # Ultimate fallback
                return series.astype(str).str.strip()

        # Apply the cleaner
        gdf[left_key] = clean_key_column(gdf[left_key])
        df[right_key] = clean_key_column(df[right_key])

        print(f"Merging on {left_key} == {right_key}")
        #Changing  the merge strategy from left to outer to keep more information 
        gdf = gdf.merge(df, left_on=left_key, right_on=right_key, how='outer')
        #df = gpd.GeoDataFrame(df,crs='EPSG:4326')
        return gdf
    # [Rest of logic for single files...]
    if df is not None and gdf is None:
         if lat_lon_cols:
            return gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[lat_lon_cols[1]], df[lat_lon_cols[0]]), crs="EPSG:4326")
    if gdf is not None:
        return gdf
    
    


class display_final_cols:
    def __init__(self, df, schema_dict):
        self.df = df
        self.schema = schema_dict
        self.mapping_widgets = {}
        self.final_mapping = {}
        self.output_area = widgets.Output()
        
        # Build the UI immediately upon creation
        self.ui = self._build_ui()

    def _build_ui(self):
        """Internal method to construct the widget interface."""
    
        user_cols = ['(None)'] + sorted(list(self.df.columns))
        
        accordion = widgets.Accordion(children=[])
        titles = []
        children = []
        
        # 1. Create Tabs for each Category
        for category, fields in self.schema.items():
            titles.append(category)
            rows = []
            
            for field_name, field_info in fields.items():
                # Auto-match logic
                default_val = '(None)'
                for col in self.df.columns:
                    if col.lower() == field_name.lower():
                        default_val = col
                        break
                dd = widgets.Dropdown(options=user_cols, value=default_val, layout=widgets.Layout(width='300px'))
                
                # UI Elements
                required = field_info.get("required", False)
                label_text = f"{field_name} *" if required else field_name

                lbl = widgets.Label(
                    value=f"{label_text}:",
                    layout=widgets.Layout(width='200px')
                )
                
    
                self.mapping_widgets[field_name] = dd
                
                required = field_info.get("required", False)
                label_text = f"{field_name} *" if required else field_name
                
                field_label = widgets.HTML(
                    f"<b>{label_text}</b> "
                    f"<span style='color:#666; font-size:0.85em;'>"
                    f"{field_info['description']}"
                    f"</span>"
                )
                
                row = widgets.HBox(
                    [field_label, dd],
                    layout=widgets.Layout(
                        justify_content='space-between',
                        align_items='center',
                        margin='6px 0'
                    )
                )
                
                rows.append(row)
            
            children.append(widgets.VBox(rows, layout=widgets.Layout(padding='10px')))

        accordion.children = tuple(children)
        for i, title in enumerate(titles):
            accordion.set_title(i, title)
            
        # 2. Create the Button
        btn = widgets.Button(
            description="Confirm Mapping", 
            button_style='success', # Make it green
            layout=widgets.Layout(width='300px', margin='10px 0px')
        )
        btn.on_click(self._on_click)
        
        # 3. Return the full layout
        container = widgets.VBox(
            [accordion, btn, self.output_area],
            layout=widgets.Layout(
                width='800px',
                margin='0 auto',
                padding='20px'
            )
            )
        return container

    def _on_click(self, b):
        """Internal callback when button is clicked."""
        with self.output_area:
            clear_output()
            self.final_mapping = {}
            assigned_cols = set()
            
            # Harvest values from dropdowns
            for field, widget in self.mapping_widgets.items():
                if widget.value != '(None)':
                    self.final_mapping[field] = widget.value
                    assigned_cols.add(widget.value)
            
            # Check for unmapped columns
            all_cols = set(self.df.columns)
            unmapped = list(all_cols - assigned_cols)
            unmapped.sort()
            
            print(f"Successfully Mapped: {len(self.final_mapping)} columns.")
            
            if unmapped:
                print("\n" + "="*40)
                print(f"UNMAPPED COLUMNS ({len(unmapped)})")
                print("The following columns from your file were NOT assigned:")
                print("="*40)
                
                # Use pprint here for clean output
                pp = pprint.PrettyPrinter(indent=4, width=80, compact=True)
                pp.pprint(unmapped)
            else:
                print("\nAll columns in the file have been mapped.")
                
            for field, widget in self.mapping_widgets.items():
                selected_col = widget.value
                if selected_col != '(None)':
                    expected_dtype = self._get_field_dtype(field)
                    actual_dtype = self.df[selected_col].dtype

                    if not self._check_dtype(actual_dtype, expected_dtype):
                        print(f"⚠ Warning: '{selected_col}' does not match expected type '{expected_dtype}'")
    
    def _get_field_dtype(self, field_name):
        for category in self.schema.values():
            if field_name in category:
                return category[field_name].get("dtype")
        return None
                        
    def _check_dtype(self, actual, expected):
        if expected == "string":
            return pd.api.types.is_string_dtype(actual)
        elif expected == "float":
            return pd.api.types.is_float_dtype(actual)
        elif expected == "int":
            return pd.api.types.is_integer_dtype(actual)
        elif expected == "datetime":
            return pd.api.types.is_datetime64_any_dtype(actual)
        else:
            return True

    def show(self):
        """Display the UI in the notebook."""
        display(self.ui)
        
    def get_mapping(self):
        """Returns the dictionary needed for pandas .rename()"""
        # Flip the dict: {User_Col : Standard_Name}
        return {v: k for k, v in self.final_mapping.items()}
    
#creating the group list
crop_to_group = {}
for group_name, group_info in utils.group_codes.items():
    for crop in group_info["crops"].keys():
        crop_to_group[crop] = group_name    
    
def crop_type_preprocess(dataset:pd.DataFrame,crop_column:str):
    data_ct = dataset.rename(columns={f"{crop_column}":"Crop_unprocessed"})
    ct_column = "Crop_unprocessed"
    #data_ct = scripts.crop_type.remove_null_ct(ct_column_name = ct_column, dataset = data_ct)  
    #getting the crops list to create group, variation and season columns
    crops_list = data_ct[ct_column].apply(scripts.crop_type.map_variations,
                                                 dict_variations = utils.crop_variations).str.split(",")  
    data_crops = crops_list.apply(
        scripts.crop_type.assign_crop_columns, 
        season_codes_dict=utils.season_codes,
        variation_codes_dict=utils.variation_codes,
        crop_to_group_dict=crop_to_group
        )
    
    print("The crop types in this dataset: ",data_crops['Crop'].value_counts())
    print("The number of variations in this dataset: ",data_crops['Crop_Variation'].value_counts())
    print("The number of group in this dataset: ",data_crops['Crop_Group'].value_counts())
    return data_crops
    
    
def assign_sow_info(dataset:pd.DataFrame):
    """
    Assigns necessary sow information to get Season_ids in the next step
    
    Parameters:
    1. Input dataframe
    
    Returns:
    Dataframe with Sow_Year column and Sow_Month, Sow_Day (if Sow_Date is available)
    
    """
    if "Sow_Date" in dataset.columns:
        dataset["Sow_Year"] = dataset["Sow_Date"].dt.year.astype("Int64")
        dataset["Sow_Month"] = dataset["Sow_Date"].dt.month.astype("Int64")
        dataset["Sow_Day"] = dataset["Sow_Date"].dt.day.astype("Int64")
        print("Columns 'Sow_Year', 'Sow_Month' and 'Sow_Date' assigned from 'Sow_Date'")
        
    else:
        if "Sow_Year" not in dataset.columns:
            dataset["Sow_Year"] = pd.NA
            print("No Sow_Date or Sow_Year found. Created Sow_Year with NA")
        else:
            print("Sow_Year already exists. Leaving as is.")
    
    return dataset    

def assign_est_sow_year(country:str,dataset:pd.DataFrame,season_year:int):
    """
    Assigns Est_Sow_Year where Sow_Year is not available (important to assign Season_id)
    
    Parameters: 
    1. Country name; currently only Ukraine has separate logic
    2. Input dataframe
    3. The crop season 
     
    Returns:
    Dataset with Est_Sow_Year column 
    
    """
    
    if "Sow_Year" not in dataset.columns:
        raise ValueError("Required column 'Sow_Year' is missing from dataset.")
    
    if country == "Ukraine" and "Crop_Season" not in dataset.columns:
        raise ValueError(
            "Column 'Crop_Season' is required for Ukraine to assign estimated sowing year."
        )
    
    dataset = dataset.copy()
    dataset["Est_Sow_Year"] = pd.Series(
    pd.NA, index=dataset.index, dtype="Int64"
    )
    mask_null = dataset["Sow_Year"].isnull()
    
    if (country == "Ukraine"):
        dataset.loc[
            mask_null & (dataset["Crop_Season"] == "Winter"),
            "Est_Sow_Year"
        ] = season_year - 1
        
        dataset.loc[
            mask_null & (dataset["Crop_Season"] != "Winter"),
            "Est_Sow_Year"
        ] = season_year
    else:
        dataset.loc[mask_null, "Est_Sow_Year"] = season_year
    print("Column 'Est_Sow_Year' successfully assigned")    
    return dataset