"""
This file gets three types of schools: public primary and secondary schools,
private schools, and colleges from the Edge OpenData API:
    - https://data-nces.opendata.arcgis.com/datasets/postsecondary-school-locations-current-1/api
    - https://data-nces.opendata.arcgis.com/datasets/public-school-characteristics-2019-20/api
    - https://data-nces.opendata.arcgis.com/datasets/private-school-locations-2019-20/api

Finally, the file outputs a .csv file that contains all of the school data

Author: Niranjan Kumawat
"""

import pandas as pd
import requests
import json

from db_init.national.google_api.utils import get_address_coordinates


def fetch_schools_data(state_code: str, county_fips: str):
    """
      Fetches hospital asset information from hospital API.
      API reference: https://www.communitybenefitinsight.org/?page=info.data_api

      For specific hospital info: api/get_hospital_data.php?hospital_id=1000

      Parameters:
          state_code(str): 2 character state postal code parameter to return
          hospitals within the provided state.
          county_fips(str): Federal Information Processing System (FIPS) Codes
          for States and Counties.
          Def- https://transition.fcc.gov/oet/info/maps/census/fips/fips.txt

      Returns:
          data_frame(dataframe): Dataframe with data
      """
    data = ""
    return data
