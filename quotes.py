from flask import Flask, render_template
import requests
import random

# Creates the Flask application instance.
app = Flask(__name__)

# Fallback static quotes used when the API is unavailable.
FALLBACK_QUOTES = [
    "The journey of a thousand miles begins with a single step.",
    "The only way to do great work is to love what you do.",
    "Success is not final, failure is not fatal: it is the courage to continue that counts.",
    "If you want to go fast, go alone. If you want to go far, go together.",
    "Wisdom is like a baobab tree; no one individual can embrace it.",
    "The axe forgets but the tree remembers.",
    "If you think you're too small to make a difference, try spending the night with a mosquito.",
    "When an old man dies, a library is burned with him.",
    "Don't think there are no crocodiles just because the water is calm.",
    "In the moment of crisis, the wise build bridges, and the foolish build dams.",
    "One who loves the vase, loves also what is inside.",
    "No shortcuts exist to the top of a palm tree."
]

# Public quotes API (no auth required)
API_URL = "https://type.fit/api/quotes"

def get_quotes_from_api(limit=10):
    """Fetch a sample of quotes from the public API. Returns a list of strings.

    Falls back to `FALLBACK_QUOTES` on any error.
    """
    try:
        resp = requests.get(API_URL, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, list) or len(data) == 0:
            raise ValueError("unexpected API response")
        sampled = random.sample(data, min(limit, len(data)))
        results = []
        for item in sampled:
            text = item.get('text') or ''
            author = item.get('author') or 'Unknown'
            results.append(f"{text} — {author}")
        return results
    except Exception:
        return random.sample(FALLBACK_QUOTES, min(limit, len(FALLBACK_QUOTES)))


@app.route('/')
def home():
    quotes = get_quotes_from_api(limit=10)
    return render_template('index.html', quote_list=quotes)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)