import feedparser
from datetime import datetime
from .config import save_config

def fetch_feeds(config: dict[str, any]) -> list[dict[str, any]]:
    result = []
    for feed in config['rss_feeds']:
        f = feedparser.parse(feed['url'])
        
        site = {
            "title": f.feed.title,
            "link": f.feed.link,
            "date": datetime(*f.feed.updated_parsed[:7]),
            "articles": []
        }
        feed['title'] = f.feed.title

        for entry in f.entries:
            # check if item is old
            date = datetime(*entry.published_parsed[:7])
            if feed['last_check'] is not None and date.replace(hour=0, minute=0, second=0) < feed['last_check'].replace(hour=0, minute=0, second=0):
                continue

            # we already had that id
            if entry.id in feed['last_ids']:
                continue
            feed['last_ids'].append(entry.id)


            article = {
                "title": entry.title,
                "link": entry.link,
                "date": date
            }

            try:
                article['summary'] = entry.summary
            except AttributeError:
                pass

            try:
                article['content'] = entry.description
            except AttributeError:
                pass

            try:
                article['content'] = entry.content
            except AttributeError:
                pass



            site['articles'].append(article)
            if len(site['articles']) >= config['max_items_per_feed']:
                break
        result.append(site)
        feed['last_check'] = datetime.now()
    save_config(config)
    return result