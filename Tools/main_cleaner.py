#!/bin/python3

import subprocess
import requests
import json
import pathlib
import logging.config
import logging.handlers
from typing import List

OK=0
COMPOSE_DOWN_FAILED=1
COMPOSE_UP_FAILED=2
MAKEMIGRATIONS_FAILED=3
MIGRATIONS_FAILED=4
DATA_CREATION_FAILED=5

logger = logging.getLogger("main_cleaner")  # __name__ is a common choice

def setup_logging():

    config_file = pathlib.Path("./logger.json")
    logging.info(config_file)
    with open(config_file) as f_in:
        config = json.load(f_in)

    config["handlers"]["file"]["filename"] = "./cleaner.log"
    logging.config.dictConfig(config)

def create_process(command: List[str], identifier: str) -> bool:

    process = subprocess.run(command)

    if process.returncode == OK:
        logger.info(f"Success - {identifier}")
        return True
    else:
        logger.error(f"Failed - {identifier} with status code {process.returncode}")

    return False

def login() -> int:

    command = ['docker', 'compose', 'down', 'postgres'] #, '&&', 'docker', 'volume', 'rm', 'trascendence_v_postgres_data']
    retval = create_process(command, "Stop postgres")

    if not retval:
        return COMPOSE_DOWN_FAILED

    command = ['docker', 'volume', 'rm', 'trascendence_v_postgres_data']
    retval = create_process(command, "Delete login database")
    if not retval:
        logger.warning("Volume for login already deleted")
        retval = True

    command = ['docker', 'compose', 'up', '-d', 'login']
    retval = create_process(command, "make login migrations")

    if not retval:
        return COMPOSE_UP_FAILED

    command = ['docker', 'compose', 'exec', 'login', 'python3', '/app/manage.py', 'makemigrations']
    retval = create_process(command, "make login migrations")

    if not retval:
        return MAKEMIGRATIONS_FAILED

    command = ['docker', 'compose', 'exec', 'login', 'python3', '/app/manage.py', 'migrate']
    retval = create_process(command, "migrate login")

    if not retval:
        return MIGRATIONS_FAILED

    command = ['docker', 'compose', 'up', '-d', 'create-data']
    retval = create_process(command, "create data")

    if not retval:
        return DATA_CREATION_FAILED


def main() -> int:

    login()

    return OK

if __name__ == "__main__":
    setup_logging()
    main()