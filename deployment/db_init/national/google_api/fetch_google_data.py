"""
This file uses the get_map_data function to call the Google API and
search our keywords within a 50000 meter radius of the center of Pittsburgh,
covering well beyond the entire area of Pittsburgh. Then, the file removes
suspected restaurants and stores and drops duplicate results from respective
keyword searches. Then, the file uses the get_location_website function to
attach
website information to the places which have a website.

Finally, the file outputs a .csv file that contains Google API data.

Author: Jameson Carter, Michaela Marincic, Niranjan Kumawat
"""
import json
import time
import pandas as pd
import requests

from deployment.db_init.constants import GOOGLE_API_KEY, OK_STATUS, REQUEST_DENIED_STATUS, \
    GOOGLE_API_PLACE_NEARBY_SEARCH, GOOGLE_API_PLACE_DETAILS, ROOT_PATH


def get_map_data(keyword: str, latitude: float, longitude: float, radius: int):
    """
      Checks if communities, source_type, and categories in data is present in
      the master tables. Returns true if included, otherwise false.

      Parameters:
          keyword(str): Keyword to search for
          latitude(float): The latitude
          longitude(float): The longitude
          radius(int): Radius to cover

      Returns:
          data_frame(dataframe): Dataframe with data
      """
    res_dataframe = pd.DataFrame(
        columns=[
            "latitude",
            "longitude",
            "address",
            "name",
            "place_id",
            "price_level"])
    # Next, we run the query again on up to two nextToken calls.
    # Google's API only produces 60 results on nearby search, with 20 in each
    # initial API call. So we check to see whether there is a nextToken for
    # each
    while True:
        params = {
            "key": GOOGLE_API_KEY,
            "location": f"{latitude},{longitude}",
            "keyword": keyword,
            "radius": radius
        }
        response = requests.get(
            GOOGLE_API_PLACE_NEARBY_SEARCH, params, timeout=10)
        result = json.loads(response.text)
        dataframe = pd.json_normalize(result['results'])
        # Separate the address from the city, first add commas to strings
        # without them so that we can use str.split()
        dataframe = dataframe.loc[:,
                                  dataframe.columns.isin(['geometry.location.lat',
                                                          'geometry.location.lng',
                                                          'vicinity',
                                                          'name',
                                                          'place_id',
                                                          'price_level',
                                                          ])]
        # Rename to make everything simpler
        dataframe = dataframe.rename(
            columns={
                "geometry.location.lat": "latitude",
                "geometry.location.lng": "longitude",
                "vicinity": "address"})
        # Merge dataframes
        res_dataframe = pd.concat([res_dataframe, dataframe])
        if "next_page_token" in result:
            params["pagetoken"] = result['next_page_token']
            time.sleep(1)
            # Need to introduce this so that API call ready for token
            print("Waiting for next page token to generate.")
            # Figure out why it runs for more iterations
            # break
        else:
            break
    res_dataframe = res_dataframe.reset_index(drop=True)
    return res_dataframe


def get_location_website(place_id: str, fields: list):
    """
      Fetches fields for given place id.

      Parameters:
          place_id(str): The place id in text
          fields(list): List of field values to be retrieved.

      Returns:
          A dataframe with the results.
    """
    params = {
        "key": GOOGLE_API_KEY,
        "place_id": place_id,
        "fields": ",".join(fields)}
    response = requests.get(GOOGLE_API_PLACE_DETAILS, params, timeout=10)
    result = json.loads(response.text)

    if result["status"] in [REQUEST_DENIED_STATUS]:
        print("Check the google API key!")
        return pd.DataFrame()  # Default empty response

    if result["status"] == OK_STATUS:
        return pd.json_normalize(result['result'])

    # Error occurred
    print(f"Error occurred while fetching website for {place_id}")
    return pd.DataFrame()  # Default empty response


def fetch_google_asset_data(
        keywords_file: str,
        latitude: float,
        longitude: float,
        radius: int):
    """
      Checks if communities, source_type, and categories in data is present in
      the master tables. Returns true if included, otherwise false.

      Parameters:
          keywords_file(str): File path of keywords
          latitude(float): The latitude
          longitude(float): The longitude
          radius(int): Radius to cover

      Returns:
          data_frame(dataframe): Dataframe with data, otherwise empty
      """
    with open(f"{ROOT_PATH}/national/google_api/keywords/{keywords_file}",
              'r', encoding='utf-8') as kw_file:
        keywords = []
        categories = []
        for line in kw_file:
            line = line.split(',')
            categories.append(line[0])
            keywords.append(line[1])

    data = pd.DataFrame()

    if not keywords:
        print("Either no keyword file name or wrong format provided")
        return data

    if not GOOGLE_API_KEY:
        print("Google API Key not set")
        return data

    for (category, keyword) in zip(categories[1:], keywords[1:]):
        dataframe = get_map_data(keyword, latitude, longitude, radius)
        dataframe["category"] = category

        data = pd.concat([data, dataframe], ignore_index=True)

    data = data.drop(data.loc[data["price_level"] >= 1].index)
    data = data.loc[:, data.columns.isin(["latitude",
                                          "longitude",
                                          "address",
                                          "name",
                                          "place_id",
                                          "category"])]

    websites = {"place_id": [], "website": []}
    for place_id in data["place_id"]:
        result = get_location_website(place_id, ["website"])

        if not result.empty:
            websites["place_id"].append(place_id)
            websites["website"].append(result.at[0, "website"])

    dataframe = pd.DataFrame.from_dict(websites)
    data = data.join(dataframe.set_index("place_id"), on="place_id")
    data.drop(columns="place_id", inplace=True)

    # Drop duplicates
    data = data.drop_duplicates()

    # Add source information
    data["source_name"] = "Google API"

    # Add a description field
    data["description"] = ""

    return data
