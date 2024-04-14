import json
from xdg_base_dirs import xdg_config_dirs
from pathlib import Path
from datetime import datetime
from copy import deepcopy

def get_config() -> dict[str, any]:
    config_files = [d / "rss2fax.json" for d in xdg_config_dirs()]
    for f in config_files:
        if f.exists():
            print(f"Loading config from {f}")
            with open(f, "r") as fp:
                data = json.load(fp)
                # now parse date items
                for rss_feed in data['rss_feeds']:
                    if rss_feed['last_check'] is not None:
                        rss_feed['last_check'] = datetime.fromisoformat(rss_feed['last_check'])
                return data

    # no config file, create a default file
    config = {
        "fax_printer": "Roger-Router-Fax",
        "rss_feeds": [
            {
                "url": "https://rss.golem.de/rss.php?feed=ATOM1.0",
                "last_check": None,
                "last_ids": []
            },
            {
                "url": "https://dunkelstern.de/atom.xml",
                "last_check": None,
                "last_ids": []
            }
        ],
        "max_items_per_feed": 5,
    }

    save_config(config)
    return get_config()

def save_config(config: dict[str, any]):
    config_files = [d / "rss2fax.json" for d in xdg_config_dirs()]
    conf = deepcopy(config)
    for rss_feed in conf['rss_feeds']:
        if rss_feed['last_check'] is not None:
            rss_feed['last_check'] = datetime.isoformat(rss_feed['last_check'])
    with open(config_files[0], "w") as fp:
        json.dump(conf, fp, indent=4)