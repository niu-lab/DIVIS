import os
import uuid


def dir_create(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def uuid_prefix():
    return uuid.uuid4().hex[:8]
