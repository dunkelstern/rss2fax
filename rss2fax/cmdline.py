from argparse import ArgumentParser
from bs4 import BeautifulSoup
from urllib import request
from .utils import list_feeds

def run_from_cmdline():
    from .config import get_config, save_config
    from .fetch import fetch_feeds
    from .render import render_feeds
    config = get_config()

    parser = ArgumentParser(prog="RSS2Fax", description="Renders RSS feeds to be sent by Fax")
    parser.add_argument(
        "--fax",
        dest="fax",
        action="store_true",
        default=False,
        help="Send fax to selected Fax printer"
    )
    parser.add_argument(
        "--pdf",
        dest="pdf",
        action="store_true",
        default=False,
        help="Render PDF, do not send Fax"
    )
    parser.add_argument(
        "--fax-printer",
        dest="printer",
        type=str,
        default=config['fax_printer'],
        help="Name of the Fax printer"
    )
    parser.add_argument(
        "--max-items",
        dest="max_items",
        type=int,
        default=config['max_items_per_feed'],
        help="How many items to render per feed",
        metavar="COUNT"
    )
    parser.add_argument(
        "--list-feeds",
        dest="list_feeds",
        default=False,
        action="store_true",
        help="List subscribed feeds"
    )
    parser.add_argument(
        "--remove-feed",
        dest="remove_feed",
        type=int,
        help="Remove subscription to feed with id given (see --list-feeds)",
        metavar="ID"
    )
    parser.add_argument(
        "--add-feed",
        dest="add_feed",
        type=str,
        help="Subscribe to a feed by URL",
        metavar='URL'
    )
    parser.add_argument(
        "--discover-feeds",
        dest="discover_feeds",
        type=str,
        help="Print out available feed URLs of a website",
        metavar='URL'
    )

    args = parser.parse_args()

    config['fax_printer'] = args.printer
    config['max_items_per_feed'] = args.max_items
    save_config(config)
    

    if args.list_feeds is True:
        # list feeds stored in config
        list_feeds(config)
        exit(0)

    if args.remove_feed is not None:
        # remove a feed from config
        del config['rss_feeds'][args.remove_feed]
        save_config(config)
        list_feeds(config)
        exit(0)

    if args.add_feed is not None:
        # add feed to config
        config["rss_feeds"].append({
            "url": args.add_feed,
            "last_ids": [],
            "last_check": None
        })
        save_config(config)
        list_feeds(config)
        exit(0)

    if args.discover_feeds:
        html = request.urlopen(args.discover_feeds).read()
        parser = BeautifulSoup(html, 'html.parser')
        links = parser.find_all('link')
        for link in links:
            if 'alternate' in link.get('rel') and link.get('type') in ['application/rss+xml', 'application/atom+xml']:
                print(link.get('href'))
        exit(0)

    if args.pdf or args.fax:
        config["pdf_only"] = args.pdf

        feeds = fetch_feeds(config)
        render_feeds(config, feeds)
    else:
        parser.print_help()