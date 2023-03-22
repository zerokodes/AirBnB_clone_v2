#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}
    __classes = {
            'BaseModel': BaseModel, 'User': User,
            'State': State, 'City': City,
            'Amenity': Amenity, 'Place': Place, 'Review': Review}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        return_all = {}

        if cls:  # valid class
            if cls.__name__ in self.__classes:
                # copy objects of cls to temp dict
                for k, v in self.__objects.items():
                    if k.split('.')[0] == cls.__name__:
                        return_all.update({k: v})
        else:  # if cls is none
            return_all = self.__objects

        return return_all

    def new(self, obj):
        """sets __object to given obj"""
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """Serialize the file to JSON file path"""
        my_dict = {}
        for key, value in self.__objects.items():
            my_dict[key] = value.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(my_dict, f)

    def reload(self):
        """deserialize the file path to JSON file path"""
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                for key, value in (json.load(f)).items():
                    value = eval(value['__class__'])(**value)
                    self.__objects[key] = value
        except FileNotFoundError:
            pass

    def close(self):
        """ reloads JSON object"""
        return self.reload()

    def delete(self, obj=None):
        """delete obj from __objects if pressent"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        del self.__objects[key]
