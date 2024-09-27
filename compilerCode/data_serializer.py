'''
this module holds different serializer functions
'''

import json
import jsonpickle
import pickle

def serialize_data(data,option=2):
    """
    This function will serialize the data
    input: data (value of data)
    output: str (string)
    """

    if option ==0:
        return json.dumps(data)
    elif option ==1:
        return jsonpickle.encode(data)
    elif option ==2:
        return pickle.dumps(data)

    return "wrong option for serialization"

def deserialize_data(data,option=2):

    """
    This function will deserialize the data
    input: data (string)
    output: data (value of data)
    """

    if option ==0:
        return json.loads(data)
    elif option ==1:
        return jsonpickle.decode(data)
    elif option ==2:
        return pickle.loads(data)

    return "wrong option for deserialization"


    