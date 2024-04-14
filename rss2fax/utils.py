
def list_feeds(config: dict[str, any]):
    for idx, feed in enumerate(config['rss_feeds']):
        if 'title' in feed:
            print(f"{idx}: {feed['title']} ({feed['url']})")
        else:
            print(f"{idx}: {feed['url']}")
