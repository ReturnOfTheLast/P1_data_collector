"""Module to interact with database
"""

# Import Modules
from pymongo import MongoClient
from pymongo.collection import Collection

def db_connect(username: str, password: str, host: str) -> MongoClient:
    """Function to connect to a mongodb database.

    Args:
        username (str): The username to login with
        password (str): The password to login with
        host (str): Hostname/address of the database

    Returns:
        MongoClient: A database client to interact with the database
    """

    # Make and return database client connection
    return MongoClient(f"mongodb://{username}:{password}@{host}:27017/")

def create_collections(
    client: MongoClient
) -> tuple[Collection, Collection, Collection, Collection]:
    """Function to get all the collections that is needed.

    Args:
        client (MongoClient): Database client to use

    Returns:
        tuple[Collection, Collection, Collection, Collection]: Collections
    """

    # Get the database and return all the collections
    db = client["scandata"]
    return (db["data_frames"],
            db["ap_data_frames"],
            db["bssid_pool"],
            db["ssid_pool"])

def handler(client: MongoClient, number: int, data: dict) -> None:
    """Function to handle and insert data frames into the database.

    Args:
        client (MongoClient): Database client to use
        number (int): Data Frame number
        data (dict): Data Frame
    """

    # Get the collections
    data_frames, ap_data_frames, bssid_pool, ssid_pool = create_collections(client)
    
    # Make list of access point data frames (subframes)
    ap_data_frame_ids = []

    # Go over all access points in data frame
    for ap in data["scan"]:

        # Check if the SSID is already registered
        ssid_data = ssid_pool.find_one({"name": ap[1]})
        if not ssid_data:
            # If not create it and get the id
            ssid_id = ssid_pool.insert_one({
                "name": ap[1]
            }).inserted_id
        else:
            # Or just get the id of the existing one
            ssid_id = ssid_data["_id"]

        # Check if the BSSID/MAC Address is already registered
        bssid_data = bssid_pool.find_one({"name": ap[0]})
        if not bssid_data:
            # If not create it and get the id
            bssid_id = bssid_pool.insert_one({
                "name": ap[0],
                "ssid": ssid_id
            }).inserted_id
        else:
            # Or just get the id of the existing one
            bssid_id = bssid_data["_id"]

        # Insert the access point data frame (subframe)
        # in the database and add the id to the list
        ap_data_frame_ids.append(
                ap_data_frames.insert_one({
                    "bssid": bssid_id,  # Id of the BSSID
                    "rssi": ap[2]       # Measured rssi signal strength in dBm
                }).inserted_id
        )

    # Create the final data frame
    data_frames.insert_one({
        "number": number,
        "location": [float(data["location"][0]), float(data["location"][1])],       # Location of scan
        "time": data["time"],               # Timestamp of scan
        "ap_data_frames": ap_data_frame_ids # List of ap data frame ids
    })
