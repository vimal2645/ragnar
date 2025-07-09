from flask import Flask, render_template, request, jsonify
import wikipedia

app = Flask(__name__)

sites = {
    "wikipedia": "https://www.wikipedia.org/",
    "google": "https://www.google.com/",
    "youtube": "https://www.youtube.com/",
    "instagram": "https://www.instagram.com/",
    "facebook": "https://www.facebook.com/",
    "twitter": "https://twitter.com/",
    "linkedin": "https://www.linkedin.com/",
    "amazon": "https://www.amazon.in/",
    "flipkart": "https://www.flipkart.com/"
}

def ask_wikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Your question is too broad. Suggestions: {e.options[:5]}"
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find anything on that topic."
    except Exception:
        return "Sorry, something went wrong searching Wikipedia."

def process_command(command):
    c_lower = command.lower().strip()

    if c_lower in sites:
        url = sites[c_lower]
        return {
            "message": f"Opening {c_lower}.",
            "url": url
        }

    wh_words = ["who is", "what is", "where is", "when is", "tell me about", "define", "explain"]
    if any(c_lower.startswith(word) for word in wh_words):
        answer = ask_wikipedia(command)
        return {
            "message": answer,
            "url": None
        }

    search_url = f"https://www.google.com/search?q={c_lower.replace(' ', '+')}"
    return {
        "message": f"I searched for {c_lower}. Here’s the link:",
        "url": search_url
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/assistant", methods=["POST"])
def assistant():
    data = request.get_json()
    user_text = data.get("text", "")
    result = process_command(user_text)
    return jsonify(result)

if __name__ == "__main__":
    # This block ensures it runs when you execute:
    # python ragnar.py
    app.run(host="0.0.0.0", port=5000, debug=True)
