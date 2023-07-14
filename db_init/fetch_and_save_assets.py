"""
Fetches assets from multiple sources, including:
1. Google API
2. Community Benefit Insight API
3. EDGE OpenData API

Author: Mihir Bhaskar, Niranjan Kumawat
"""

from datetime import datetime, timezone
from pandas import DataFrame

from db_init.constants import TANGIBLE_ASSET, ASSETS_DATA_LOC, CONFIGURATION
from db_init.national.fetch_national_assets import fetch_national_assets


def de_duplication(data: DataFrame, cols: list):
    """
      Handling duplicate information in data.

      Parameters:
          data(DataFrame): Dataframe with duplicate information
          cols(list): Columns considered for de-duplication

      Returns:
          De-duplicated dataframe
    """
    # Need to sort out duplicates that arise from the same asset coming
    # from two different sources (Maps API and getSchools/getHospitals),
    # referring to the same category
    # For these cases, these two rows need to be collapsed into one
    # If time: sometimes, one data source will have more info than the
    # other (e.g. website vs. no website), so if this info can also be
    # preserved/collapsed into one row that would be great

    # Asset ID (uuid) needs to be created on the basis of asset name +
    # location

    # There are cases where the asset name is the same, but there could
    # be multiple locations (e.g. multiple outlets of the same store)
    # There are also cases where the location is the same, but there are
    # two different assets in that location - e.g. an elementary school,
    # and a middle school by different names

    # Right now, in nationalData, there are multiple rows for the same
    # asset if it has multiple categories, and the only thing
    # varying across these rows is the category. The same asset ID needs
    # to be assigned for these rows referring to the same asset - right
    # now, a new uuid is created for every row in the table.

    # This is some nice code to look for similar locations and flag them,
    # based on similar lat/longs:
    # https://stackoverflow.com/questions/54867061/how-to-detect-almost
    # -duplicate-locations-in-a-pandas-dataframe

    # Basic de-duplication
    data = data.drop_duplicates(subset=cols)

    return data


if __name__ == "__main__":
    communities = CONFIGURATION["communities"]
    for community in communities:
        print(f"Adding data for {community['name']}")

        county_fips = community["countyFIPS"]
        state_code = community["stateCode"]
        county_name = community["countyName"]
        latitude = community["latitude"]
        longitude = community["longitude"]
        radius = community["radius"]
        # CSV file of format "<community>.csv"
        keywords_filename = community["keywordsFileName"]

        # Fetch national assets
        national_data = fetch_national_assets(
            state_code,
            (county_fips, county_name),
            keywords_filename,
            (latitude, longitude),
            radius)
        # Incorporated Place GEOID
        # Sourced from https://geocoding.geo.census.gov/geocoder/geographies
        # /onelineaddress?form
        national_data["com_name"] = community["name"]
        national_data["com_geo_id"] = community["communityGeoId"]

        national_data["type"] = TANGIBLE_ASSET
        national_data["timestamp"] = datetime.now(timezone.utc)
        national_data["status"] = 0

        asset_data = national_data  # Add from other sources here

        # Handling duplicate information
        asset_data = de_duplication(asset_data,
                                    ["name",
                                     "category",
                                     "description",
                                     "address",
                                     "latitude",
                                     "longitude",
                                     "website"])

        # Drop index
        asset_data.reset_index(drop=True, inplace=True)

        # Save assets before uploading
        asset_data.to_csv(ASSETS_DATA_LOC, sep='\t', index=False)
        print(f"Assets are saved to {ASSETS_DATA_LOC}")
