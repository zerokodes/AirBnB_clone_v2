#!/usr/bin/python3
""" """
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os


class test_basemodel(unittest.TestCase):
    """unittest for testing the BaseModel class """

    @classmethod
    def setUpClass(cls):
        """setup for the test """
        cls.base = BaseModel()
        cls.base.name = "Sepi"
        cls.base.num = 20

    @classmethod
    def tearDown(cls):
        " test BaseModel teardown"
        del cls.base

    def tearDown(self):
        "tear down"
        try:
            os.remove('file.json')
        except Exception:
            pass

    @unittest.skipIf(os.environ['HBNB_TYPE_STORAGE'] == 'db', 'Test storage')
    def test_save(self):
        """ Test if the save works"""
        self.base.save()
        self.assertNotEqual(self.base.created_at, self.base.updated_at)
