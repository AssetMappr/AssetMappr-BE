"""
This file contains utilities specific to google apis.

Author: Niranjan Kumawat
"""
import json
import requests

from deployment.db_init.constants import GOOGLE_API_KEY, \
    REQUEST_DENIED_STATUS, OK_STATUS, \
    GOOGLE_API_GEOCODE


def get_address_coordinates(address: str) -> tuple:
    """
      Checks if communities, source_type, and categories in data is present in
      the master tables. Returns true if included, otherwise false.

      Parameters:
          address(str): Address for which coordinates are required.

      Returns:
          (latitude, longitude, place_id) (tuple): If found, a tuple of latitude,
          longitude, and place_id for given address, otherwise None.
    """
    params = {"key": GOOGLE_API_KEY, "address": address}
    response = requests.get(
        url=GOOGLE_API_GEOCODE,
        params=params,
        timeout=10)
    result = json.loads(response.text)

    if result["status"] in [REQUEST_DENIED_STATUS]:
        print("Check the google API key!")
        return None

    if result["status"] == OK_STATUS:
        results = result["results"][0]
        latitude = results["geometry"]["location"]["lat"]
        longitude = results["geometry"]["location"]["lng"]
        place_id = results["place_id"]
        return latitude, longitude, place_id

    # Error occurred
    print(f"Error occurred while fetching coordinates for {address}")
    return None
