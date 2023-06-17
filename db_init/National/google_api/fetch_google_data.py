"""
This file uses the get_map_data function to call the Google API and
search our keywords within a 50000 meter radius of the center of Pittsburgh,
covering well beyond the entire area of Pittsburgh. Then, the file removes
suspected restaurants and stores and drops duplicate results from respective
keyword searches. Then, the file uses the get_location_website function to
attach
website information to the places which have a website.

Finally, the file outputs a .csv file that contains Google API data.

Author: Niranjan Kumawat
"""

import pandas as pd
import time
import requests
import json

from db_init.constants import GOOGLE_API_KEY


def get_map_data(latitude, longitude, keyword, radius):
    """
      Checks if communities, source_type, and categories in data is present in
      the master tables. Returns true if included, otherwise false.

      Parameters:
          latitude(float): The latitude
          longitude(float): The longitude
          keyword(str): Keyword to search for
          radius(int): Radius to cover

      Returns:
          data_frame(dataframe): Dataframe with data
      """
    # TODO: Empty dataframe w/ columns
    res_dataframe = None
    while True:
        params = {
            "key": GOOGLE_API_KEY,
            "location": f"{latitude},{longitude}",
            "keyword": keyword,
            "radius": radius
        }
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        response = requests.get(url, params)
        result = json.loads(response.text)
        df = pd.json_normalize(result['results'])
        # Separate the address from the city, first add commas to strings
        # without them so that we can use str.split()
        df = df.loc[:,
                    df.columns.isin(['geometry.location.lat',
                                     'geometry.location.lng',
                                     'vicinity',
                                     'name',
                                     'place_id',
                                     'price_level',
                                     ])]
        # Rename to make everything simpler
        df = df.rename(columns={"geometry.location.lat": "latitude",
                                "geometry.location.lng": "longitude",
                                "vicinity": "address"})
        # TODO: Merge dataframes
        res_dataframe = df
        if "next_page_token" in result:
            params["pagetoken"] = result['next_page_token']
            # Need to introduce this so that API call ready for token
            time.sleep(2) # TODO: Determine good number for this
        else:
            break

    return res_dataframe
