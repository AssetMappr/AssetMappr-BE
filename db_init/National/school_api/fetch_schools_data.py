"""
This file gets three types of schools: public primary and secondary schools,
private schools, and colleges from the Edge OpenData API:
    - https://data-nces.opendata.arcgis.com/datasets/postsecondary-school-locations-current-1/api
    - https://data-nces.opendata.arcgis.com/datasets/public-school-characteristics-2019-20/api
    - https://data-nces.opendata.arcgis.com/datasets/private-school-locations-2019-20/api

Finally, the file outputs a .csv file that contains all of the school data

Author: Jameson Carter, Niranjan Kumawat
"""

import pandas as pd
import requests
import json


def fetch_private_schools(county_fips: str):
    """
          Fetches private schools data.

          Parameters:
              county_fips(str): Federal Information Processing System (FIPS)
              Codes

          Returns:
              data_frame(dataframe): Dataframe with data
    """
    url = f"https://nces.ed.gov/opengis/rest/services/K12_School_Locations" \
          f"/EDGE_GEOCODE_PRIVATESCH_1920/MapServer/0/query?where=CNTY%20%3" \
          f"D%20\'{county_fips}\'&outFields=NAME,STREET,CITY,LAT," \
          f"LON&outSR=4326&f=json"

    response = requests.get(url, timeout=5)
    result = json.loads(response.text)
    df = pd.json_normalize(result["features"])

    if not df.empty:
        df["category"] = "Education and workforce development"
        df["description"] = "Private school"
        df["website"] = ""
        df.rename(columns={"attributes.NAME": "name",
                           "attributes.STREET": "address",
                           "attributes.CITY": "city",
                           "attributes.LAT": "latitude",
                           "attributes.LON": "longitude"}, inplace=True)
        df["address"] = df["address"] + ", " + df["city"]

        return df[["name", "category", "description", "address",
                   "latitude", "longitude", "website"]]
    else:
        column_names = ["name", "category", "description", "address",
                        "latitude", "longitude", "website"]
        df = pd.DataFrame(columns=column_names)
        return df


def fetch_public_schools(state_code: str, county_name: str):
    """
        Fetches public schools data.

        Parameters:
          state_code(str): 2 character state postal code parameter to return
          hospitals within the provided state.
          county_name(str): 2 character state postal code parameter to return
          hospitals within the provided state. Check https://data-nces.opendata.arcgis.com/datasets/nces::public-school-characteristics-2019-20/explore?location=36.667912%2C-96.401190%2C16.00 for exact names.

        Returns:
            data_frame(dataframe): Dataframe with data
    """
    url = f"https://nces.ed.gov/opengis/rest/services/K12_School_Locations" \
          f"/EDGE_ADMINDATA_PUBLICSCH_1920/MapServer/0/query?where=STABR%20" \
          f"%3D%20'{state_code}'%20AND%20NMCNTY%20%3D%20'" \
          f"{county_name}'&outFields=SCH_NAME,SCHOOL_LEVEL,LATCOD,LONCOD," \
          f"SCHOOL_TYPE_TEXT,SY_STATUS_TEXT,LSTREET1,LCITY,NMCNTY," \
          f"STABR&outSR=4326&f=json"

    # Call the EDGE OpenData API
    response = requests.get(url, timeout=5)
    result = json.loads(response.text)
    df = pd.json_normalize(
        result["features"])  # normalize json file into pandas

    if not df.empty:  # If there ARE results, continue
        df["category"] = "Education and workforce development"
        df["description"] = "Public school"
        df["website"] = ""
        df.rename(columns={"attributes.SCH_NAME": "name",
                           "attributes.LSTREET1": "address",
                           "attributes.LCITY": "city",
                           "attributes.LATCOD": "latitude",
                           "attributes.LONCOD": "longitude"}, inplace=True)

        df["address"] = df["address"] + ", " + df["city"]

        df = df[["name", "category", "description",
                 "address", "latitude", "longitude", "website"]]

        return df

    else:  # Otherwise, return empty dataframe
        column_names = ["name", "category", "description", "address",
                        "latitude", "longitude", "website"]
        df = pd.DataFrame(columns=column_names)
        return df


def fetch_post_sec_schools(county_fips: str):
    """
          Fetches post secondary schools data.

          Parameters:
              county_fips(str): Federal Information Processing System (FIPS)
              Codes

          Returns:
              data_frame(dataframe): Dataframe with data
    """
    url = f"https://services1.arcgis.com/Ua5sjt3LWTPigjyD/arcgis/rest" \
          f"/services/Postsecondary_School_Locations_Current/FeatureServer/0" \
          f"/query?where=CNTY%20%3D%20'{county_fips}'&outFields=NAME,STREET," \
          f"CITY,LAT,LON&outSR=4326&f=json"

    response = requests.get(url, timeout=5)
    result = json.loads(response.text)
    df = pd.json_normalize(result["features"])

    if not df.empty:
        df["category"] = "Education and workforce development"
        df["description"] = "Postsecondary school"
        df["website"] = ""
        df.rename(columns={"attributes.NAME": "name",
                           "attributes.STREET": "address",
                           "attributes.CITY": "city",
                           "attributes.LAT": "latitude",
                           "attributes.LON": "longitude"}, inplace=True)
        df["address"] = df["address"] + ", " + df["city"]

        return df[["name", "category", "description", "address",
                   "latitude", "longitude", "website"]]
    else:
        column_names = ["name", "category", "description", "address",
                        "latitude", "longitude", "website"]
        df = pd.DataFrame(columns=column_names)
        return df


def fetch_schools_asset_data(
        state_code: str,
        county_fips: str,
        county_name: str):
    """
      Fetches schools data from 3 schools API.

      Parameters:
          state_code(str): 2 character state postal code parameter to return
          hospitals within the provided state.
          county_fips(str): Federal Information Processing System (FIPS) Codes
          for States and Counties.
          Def- https://transition.fcc.gov/oet/info/maps/census/fips/fips.txt
          county_name(str): The name of the county

      Returns:
          data_frame(dataframe): Dataframe with data
      """
    df_private = fetch_private_schools(county_fips)
    df_public = fetch_public_schools(state_code, county_name)
    df_post_sec = fetch_post_sec_schools(county_fips)
    data = pd.concat([df_private, df_public, df_post_sec])

    data["source_name"] = "NCES Common Core of Data API"
    data["name"] = data["name"].str.title()

    # print("If any of these searches yield no results, make sure your county "
    #       "names, county codes, and state codes are correct")
    # print(f"Found {df_private.shape[0]} private schools")
    # print(f"Found {df_public.shape[0]} public schools")
    # print(f"Found {df_post_sec.shape[0]} post-secondary schools")

    return data
