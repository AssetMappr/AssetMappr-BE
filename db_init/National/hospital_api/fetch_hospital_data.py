"""
This file gets hospitals across the US from the Community Benefit API:
- About: https://www.communitybenefitinsight.org/?page=info.data_api
- API: http://www.communitybenefitinsight.org/api/get_hospitals.php

Author: Michaela Marincic, Niranjan Kumawat
"""

import pandas as pd
import requests
import json

from db_init.national.google_api.utils import get_address_coordinates


def fetch_hospitals_asset_data(state_code: str, county_fips: str):
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
    url = f"https://www.communitybenefitinsight.org/api/get_hospitals.php?state={state_code}"
    response = requests.get(url)
    data = pd.json_normalize(json.loads(response.text))
    column_names = ["asset_name", "category", "description", "address",
                    "latitude", "longitude", "website", "source_type"]
    if data.empty:
        print(f"No hospital data available for state {state_code}")
        data = pd.DataFrame(columns=column_names)
    else:
        # Drop hospital in other counties
        data = data.drop(
            data.loc[data["fips_state_and_county_code"] != county_fips].index)

        # Fill remaining asset fields
        data["category"] = "Healthcare"
        data["description"] = "Hospital"
        data["website"] = ""
        data["source_type"] = "Community Benefit Hospitals API"
        data["address"] = data["street_address"] + \
            "," + data["city"] + "," + data["state"]
        data = data.rename(columns={"name": "asset_name"})

        lat = []
        long = []
        for i in data["address"]:
            la, lo, _ = get_address_coordinates(i)[0]
            lat.append(la)
            long.append(lo)

        data["latitude"] = lat
        data["longitude"] = long
        data = data[column_names]

    return data
