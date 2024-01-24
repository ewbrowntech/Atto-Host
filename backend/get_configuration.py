"""
get_configuration.py

@Author: Ethan Brown - ethan@ewbrowntech.com

Get the configuration for Atto-Host

Copyright (C) 2024 by Ethan Brown
All rights reserved. This file is part of the Atto-Host project and is released under
the MIT License. See the LICENSE file for more details.
"""
import os
import json


def get_config():
    config_filepath = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_filepath, "r") as config_file:
        config = json.loads(config_file.read())
    return config
