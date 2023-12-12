import os
import shelve
import uuid

databasePath = os.getenv("STORAGE_DATABASE")
INSTALLATION_ID = "installation_id"


def get_installation_id():
    return "n/a"
    with shelve.open(databasePath) as storage:
        installation_id = storage.get(INSTALLATION_ID)
        if installation_id is None:
            installation_id = uuid.uuid4()
            storage[INSTALLATION_ID] = installation_id

        return installation_id
