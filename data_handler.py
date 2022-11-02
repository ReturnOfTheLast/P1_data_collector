# Import Modules
from pymongo import MongoClient

def db_connect() -> MongoClient:
    return MongoClient("mongodb://root:password@localhost:27017/")

client = db_connect()

def create_collections() -> tuple:
    global client
    db = client["scandata"]
    return db["data_frames"], db["ap_data_frames"], db["bssid_pool"], db["ssid_pool"]

"""
data = {
    "scandata": [
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

def handler(data: dict):
    global client
    data_frames, ap_data_frames, bssid_pool, ssid_pool = create_collections()

    ap_data_frame_ids = []

    for ap in data["scandata"]:
        ssid_data = ssid_pool.find_one({"name": ap[1]})
        if not ssid_data:
            ssid_id = ssid_pool.insert_one({"name": ap[1]}).inserted_id
        else:
            ssid_id = ssid_data["_id"]

        bssid_data = bssid_pool.find_one({"name": ap[0]})
        if not bssid_data:
            bssid_id = bssid_pool.insert_one({"name": ap[0], "ssid": ssid_id}).inserted_id
        else:
            bssid_id = bssid_data["_id"]

        ap_data_frame = {
                "bssid": bssid_id,
                "rssi": ap[2]
        }

        ap_data_frame_ids.append(ap_data_frames.insert_one(ap_data_frame).inserted_id)
    
    data_frame = {
            "location": data["location"],
            "time": data["time"],
            "ap_data_frames": ap_data_frame_ids
    }

    data_frames.insert_one(data_frame)
