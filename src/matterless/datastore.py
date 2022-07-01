import os

import appdirs
from cachetools import LRUCache
from shelved_cache import PersistentCache


USERAPPDIRS = appdirs.AppDirs("matterless", "Mark Gomersbach")
DATASHELVE = USERAPPDIRS.user_cache_dir + "/matterless"

os.makedirs(os.path.dirname(DATASHELVE), exist_ok=True)

cache = {
    "my_user": PersistentCache(
        LRUCache, filename=DATASHELVE + "_my_user.shelf", maxsize=8
    ),
    "my_teams": PersistentCache(
        LRUCache, filename=DATASHELVE + "_my_teams.shelf", maxsize=8
    ),
    "known_users": PersistentCache(
        LRUCache, filename=DATASHELVE + "_known_users.shelf", maxsize=8
    ),
    "human_channels": PersistentCache(
        LRUCache, filename=DATASHELVE + "_human_channels.shelf", maxsize=8
    ),
    "channels": PersistentCache(
        LRUCache, filename=DATASHELVE + "_channels.shelf", maxsize=8
    ),
    "posts": PersistentCache(
        LRUCache, filename=DATASHELVE + "_posts.shelf", maxsize=8
    ),
}
