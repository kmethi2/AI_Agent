import feedparser

# Define your news categories and RSS feeds
NEWS_FEEDS = {
    "World": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "Technology": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "Science": "https://www.sciencedaily.com/rss/top/science.xml",
    "Business": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
    "Sports": "https://www.espn.com/espn/rss/news",
}

def get_headlines():
    all_headlines = {}

    for category, url in NEWS_FEEDS.items():
        feed = feedparser.parse(url)
        articles = []
        for entry in feed.entries[:5]:  # limit to 5 top headlines per category
            articles.append({
                "title": entry.title,
                "link": entry.link
            })
        all_headlines[category] = articles

    return all_headlines

def display_headlines():
    headlines = get_headlines()
    print("\n=== 🗞️  Today's Top Headlines ===\n")
    for category, articles in headlines.items():
        print(f"--- {category} ---")
        for article in articles:
            print(f"• {article['title']}")
            print(f"  {article['link']}")
        print()
    print("===============================\n")

if __name__ == "__main__":
    display_headlines()
