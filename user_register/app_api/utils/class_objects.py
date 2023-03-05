""" class objects"""
import json


class MakeObj:
    """make object class"""

    def __init__(self, dict):
        """init"""
        self.__dict__.update(dict)

    def convert_to_obj(dict):
        """convert dictionary to objects"""
        return json.loads(json.dumps(dict), object_hook=MakeObj)

    def convert_to_dict(obj):
        """convert objects to dictionary"""
        return json.loads(json.dumps(obj, default=lambda o: o.__dict__))
