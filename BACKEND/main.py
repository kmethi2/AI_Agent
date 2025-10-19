import random
from get_news import get_headlines
from summarize import summarize_text
from storage import save_daily_headlines, save_daily_deep_dive
from newspaper import Article

MAX_CHARS = 3000
MAX_ATTEMPTS = 5

def get_random_open_article(headlines):
    """
    Picks a random article and tries to download full text.
    Skips paywalled, blocked, or empty articles.
    """
    all_articles = [a for cat in headlines.values() for a in cat]

    for _ in range(MAX_ATTEMPTS):
        article_info = random.choice(all_articles)
        try:
            article = Article(article_info['link'])
            article.download()
            article.parse()
            full_text = article.text.strip()
            if full_text:
                return article_info, full_text[:MAX_CHARS]
        except Exception:
            continue

    # Fallback to headline if all attempts fail
    article_info = random.choice(all_articles)
    return article_info, article_info['title']

def run_daily_agent():
    # 1️⃣ Fetch today's headlines
    headlines = get_headlines()
    print("\n=== 🗞️ Today's Headlines ===\n")
    for category, articles in headlines.items():
        print(f"--- {category} ---")
        for article in articles:
            print(f"• {article['title']}")
            print(f"  {article['link']}")
        print()
    
    # 2️⃣ Save headlines
    save_daily_headlines(headlines)

    # 3️⃣ Pick and summarize a deep dive
    article_info, full_text = get_random_open_article(headlines)
    print("\n=== 🧠 Today's Deep Dive ===\n")
    print(f"Headline: {article_info['title']}")
    print(f"Source: {article_info['link']}\n")

    print("Generating summary...\n")
    try:
        summary = summarize_text(full_text)
    except Exception as e:
        summary = f"Error generating summary: {e}"

    print("📝 Summary:")
    print(summary)

    # 4️⃣ Save deep dive
    deep_dive_data = {
        "headline": article_info['title'],
        "link": article_info['link'],
        "summary": summary
    }
    save_daily_deep_dive(deep_dive_data)

    print("\n✅ Daily agent run complete!")

if __name__ == "__main__":
    run_daily_agent()

