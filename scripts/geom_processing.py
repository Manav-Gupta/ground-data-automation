import geopandas as gpd
import shapely
import s2cell

TOLERANCE = 1e-6

def check_invalid_geoms(gdf:gpd.GeoDataFrame):
    """
    Check and separate invalid and null geometries from a GeoDataFrame.

    Parameters:
        gdf (gpd.GeoDataFrame) : Input GeoDataFrame.

    Returns:
        tuple: (invalid_geometries_gdf, valid_geometries_gdf)

    Raises:
        TypeError: If input is not a GeoDataFrame
        ValueError: If 'geometry' column is missing

    """
    if not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("Input must be a GeoDataFrame")
    if 'geometry' not in gdf.columns:
        raise ValueError("Input GeoDataFrame must have a 'geometry' column")

    invalid_geoms = gdf[~gdf.geometry.notnull()]
    valid_geoms = gdf[gdf.geometry.notnull()].copy().reset_index(drop=True)
 
    return invalid_geoms,valid_geoms

def check_repeating_geoms(gdf:gpd.GeoDataFrame):
    """
    Check and diplay the repeating geometry indexes from a GeoDataFrame.

    Parameters:
        gdf (gpd.GeoDataFrame) : Input GeoDataFrame.

    Returns:
        tuple: (duplicate_geometries_indexes)

    Raises:
        TypeError: If input is not a GeoDataFrame
        ValueError: If 'geometry' column is missing

    """
    if not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("Input must be a GeoDataFrame")
    if 'geometry' not in gdf.columns:
        raise ValueError("Input GeoDataFrame must have a 'geometry' column")
    
    duplicate_pairs=[]
    sindex = gdf.sindex
    for idx, geom in gdf.geometry.items():
        possible_matches_index = sindex.intersection(geom.bounds)
        possible_matches_index = [int(i) for i in possible_matches_index if i!=idx]

        for i in possible_matches_index:
            if i> idx and geom.equals_exact(gdf.geometry.iloc[i],tolerance=TOLERANCE):
                duplicate_pairs.append((idx,i))

    return duplicate_pairs


def check_repeating_geoms_s2cell(gdf:gpd.GeoDataFrame, col_name:str, granularity:int):
    """
    
    Check and display the repeating geometry dataframe and assign the geom ids

    Parameters: 
    gdf (gpd.GeodataFrame) : Input GoeDataFrame

    Returns:
    
    1. Repeated GeoDataFrame with the s2cell ids
    2. Original GeoDataFrame with the s2cell ids

    Raises:
        TypeError: If input is not a GeoDataFrame
        ValueError: If 'geometry' column is missing
    
    """
    if not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("Input must be a GeoDataFrame")
    if 'geometry' not in gdf.columns:
        raise ValueError("Input GeoDataFrame must have a 'geometry' column")

    centroids = gdf.geometry.centroid
    gdf['lat'] = centroids.y
    gdf['lon'] = centroids.x
    gdf[col_name] = gdf.apply(
    lambda row: s2cell.lat_lon_to_token(row['lat'], row['lon'], granularity),
    axis=1
)
    repeating = gdf[gdf[col_name].duplicated(keep=False)]
    if repeating.empty:
        print("No duplicated geoms in this dataset")
    else:
        print(repeating)
    print("Geom ids assigned to the geodataframe")
    print("\n")
    return repeating,gdf


def polygon_remove_z(polygon:shapely.Polygon):
    return shapely.Polygon([coord[:2] for coord in polygon.exterior.coords[:]])

def geometry_remove_z(geometry:shapely.Geometry):
    if geometry.geom_type == 'MultiPolygon':
        geoms_wo_z = []
        for geom in geometry.geoms:
            geoms_wo_z.append(polygon_remove_z(polygon = geom))
        return shapely.MultiPolygon(geoms_wo_z)
    
    elif geometry.geom_type == 'Polygon':
        return polygon_remove_z(polygon = geometry)
    
    else:
        raise NotImplementedError(f'geometry.geom_type = {geometry.geom_type}')
    
