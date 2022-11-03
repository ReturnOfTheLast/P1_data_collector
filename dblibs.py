# Import Modules
from pymongo import MongoClient

# Function to connect the database
# TODO: Make this not hardcoded
def db_connect(username: str, password: str, host: str) -> MongoClient:
    return MongoClient(f"mongodb://{username}:{password}@{host}:27017/")

# Make client
client = db_connect("root", "password", "localhost")

# Function to get the correct collections
def create_collections() -> tuple:
    global client
    db = client["scandata"]
    return (db["data_frames"],
            db["ap_data_frames"],
            db["bssid_pool"],
            db["ssid_pool"])

"""
Sample data frame
data = {
    "scan": [
        ["000000000001", "SSID1", -10],
        ["000000000002", "SSID2", -10],
        ["000000000003", "SSID3", -10],
        ["000000000004", "SSID4", -10],
        ["000000000005", "SSID5", -10],
        ["000000000006", "SSID6", -10],
        ["000000000007", "SSID7", -10],
        ["000000000008", "SSID8", -10],
        ["000000000009", "SSID9", -10],
        ["000000000010", "SSID10", -10]
    ],
    "location": [0, 0, 0],
    "time": 0
}
"""

# Function to handle a data frame
def handler(data: dict):
    # Get the collections
    data_frames, ap_data_frames, bssid_pool, ssid_pool = create_collections()
    
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
        "location": data["location"],       # Location of scan
        "time": data["time"],               # Timestamp of scan
        "ap_data_frames": ap_data_frame_ids # List of ap data frame ids
    })