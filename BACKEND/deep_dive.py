import random
from newspaper import Article
from get_news import get_headlines
from summarize import summarize_text
from storage import save_daily_deep_dive

MAX_CHARS = 3000  # limit for summarizer
MAX_ATTEMPTS = 5  # max tries to get an open-access article

def get_random_open_article():
    """
    Picks a random article and tries to download full text.
    Skips articles that fail (403, paywall, empty text, etc.)
    """
    headlines = get_headlines()
    all_articles = [a for cat in headlines.values() for a in cat]

    for _ in range(MAX_ATTEMPTS):
        article_info = random.choice(all_articles)
        try:
            article = Article(article_info['link'])
            article.download()
            article.parse()
            full_text = article.text.strip()
            if full_text:  # only use non-empty text
                return article_info, full_text[:MAX_CHARS]
        except Exception:
            continue  # try another article

    # If all attempts fail, fallback to headline only
    article_info = random.choice(all_articles)
    return article_info, article_info['title']

def run_deep_dive():
    article_info, full_text = get_random_open_article()

    print("=== 🧠 Today's Deep Dive ===\n")
    print(f"Headline: {article_info['title']}")
    print(f"Source: {article_info['link']}\n")

    print("Generating summary...\n")
    try:
        summary = summarize_text(full_text)
    except Exception as e:
        summary = f"Error generating summary: {e}"

    print("📝 Summary:")
    print(summary)

    deep_dive_data = {
        "headline": article_info['title'],
        "link": article_info['link'],
        "summary": summary
    }
    save_daily_deep_dive(deep_dive_data)

    print("\n✅ Deep dive complete!")

if __name__ == "__main__":
    run_deep_dive()

