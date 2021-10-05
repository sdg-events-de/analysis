import hashlib
import json

# Generate a hash ID from a dictionary
# The same dictionary will yield the same hash ID, but two different
# dictionaries will return two different hash IDs.
def hash_from_dict(dict):
    json_string = json.dumps(dict, sort_keys=True, default=str)
    return hashlib.sha256(bytes(json_string, encoding="utf-8")).hexdigest()