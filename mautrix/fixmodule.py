# This is a script that fixes the __module__ tags in mautrix-python and some libraries.
# It's used to help Sphinx/autodoc figure out where the things are canonically imported from
# (by default, it shows the exact module they're defined in rather than the top-level import path).

from types import FunctionType, ModuleType
from typing import NewType

import aiohttp

from . import types, bridge, client, crypto, errors, appservice
from .crypto import attachments
from .util import async_db, config, db, formatter, logging


def _fix(obj: ModuleType) -> None:
    for item_name in getattr(obj, "__all__", None) or dir(obj):
        item = getattr(obj, item_name)
        if isinstance(item, (type, FunctionType, NewType)):
            # Ignore backwards-compatibility imports like the BridgeState import in mautrix.bridge
            if (
                item.__module__.startswith("mautrix")
                and not item.__module__.startswith(obj.__name__)
            ):
                continue

            item.__module__ = obj.__name__
        # elif type(item).__module__ == "typing":
        #     print(obj.__name__, item_name, type(item))


_things_to_fix = [types, bridge, client, crypto, attachments, errors, appservice, async_db,
                  config, db, formatter, logging, aiohttp]

for mod in _things_to_fix:
    _fix(mod)
