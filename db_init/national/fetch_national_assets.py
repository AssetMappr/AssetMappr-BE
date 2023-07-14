"""
Fetches national assets from multiple sources, including:
1. Google API
2. Community Benefit Insight API
3. EDGE OpenData API

Author: Niranjan Kumawat
"""
import pandas as pd

from db_init.national.google_api.fetch_google_data import \
    fetch_google_asset_data
from db_init.national.hospital_api.fetch_hospital_data import \
    fetch_hospitals_asset_data
from db_init.national.school_api.fetch_schools_data import \
    fetch_schools_asset_data


def fetch_national_assets(
        state_code: str,
        county_details: tuple,
        keywords_filename: str,
        coordinates: tuple,
        radius: int):
    """
      Checks if communities, source_type, and categories in data is present in
      the master tables. Returns true if included, otherwise false.

      Parameters:
          state_code(str): 2 character state postal code
          county_details(tuple): FIPS, County name
          keywords_filename(str): File name at './national/google_api/keywords/*'
          coordinates(tuple): latitude, longitude
          radius(int): Radius to cover

      Returns:
          data_frame(dataframe): Dataframe with data
    """
    (county_fips, county_name) = county_details
    (latitude, longitude) = coordinates
    # Asset information extracted using keywords from Google API
    df_google = fetch_google_asset_data(
        keywords_filename, latitude, longitude, radius)
    # Hospitals asset information
    df_hospitals = fetch_hospitals_asset_data(state_code, county_fips)
    # Schools asset information
    df_schools = fetch_schools_asset_data(state_code, county_fips, county_name)

    return pd.concat([df_google, df_hospitals, df_schools])
