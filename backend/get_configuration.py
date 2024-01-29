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
    config_path = os.environ.get("CONFIG_PATH")
    # If a config_path is not specified in the environment variables, use the default config
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
    elif not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file was not found at {config_path}")
    elif not os.path.isfile(config_path):
        raise IsADirectoryError(
            f"Config file path does not represent a file: {config_path}"
        )
    elif os.path.getsize(config_path) == 0:
        raise ValueError(f"Config file is empty: {config_path}")
    # Attempt to load the JSON file
    try:
        with open(config_path, "r") as config_file:
            config = json.loads(config_file.read())
    except PermissionError:
        raise PermissionError(f"Permission denied: {config_path}")
    except UnicodeDecodeError:
        raise UnicodeDecodeError(
            f"File encoding issue with {config_path}. Expected encoding: {encoding}."
        )
    except json.JSONDecodeError:
        raise ValueError(f"The config file at {config_path} is not a valid JSON file.")
    except Exception as e:
        # Catch any other exception and raise it
        raise e

    if is_config_valid(config):
        return config


def is_config_valid(config):
    missing_fields = [
        field
        for field in ["allowed_mimetypes", "allowed_extensions", "filesize_limit"]
        if field not in config
    ]
    if missing_fields:
        raise KeyError(
            f"Missing required configuration fields: {', '.join(missing_fields)}"
        )

    # Check if fields A and B are lists
    if not isinstance(config.get("allowed_mimetypes", None), list):
        raise TypeError("'allowed_mimetypes'' must be a list.")

    if not isinstance(config.get("allowed_extensions", None), list):
        raise TypeError("'allowed_extensions' must be a list.")

    # Check if field C is an integer greater than 0
    if (
        not isinstance(config.get("filesize_limit", None), int)
        or config["filesize_limit"] <= 0
    ):
        raise ValueError("'filesize_limit'' must be an integer greater than 0.")

    return True
