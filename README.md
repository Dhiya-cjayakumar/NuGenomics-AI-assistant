
# NuGenomics-AI-Assistant

**NuGenomics-AI-Assistant** is a dual-agent web application built with Flask that:

1. **Customer Support Agent** – Answers NuGenomics FAQs by **live-scraping** the official FAQ page on every request so answers stay up-to-date.
2. **Genetic Wellness Agent** – Handles general genetics & wellness questions via **Google Agent Development Kit (ADK)** powered by Gemini (Vertex AI).

A single HTML/Tailwind front-end lets users either pick an agent manually or use an **auto-detect classifier** that routes the question to the most relevant agent.

---

##  Features

| Feature                    | Description                                                                                                                        |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Live FAQ Scraping**      | BeautifulSoup pulls fresh Q\&A pairs from [NuGenomics FAQ](https://www.nugenomics.in/faqs/) at runtime.                            |
| **Semantic FAQ Matching**  | Custom semantic groups + fuzzy matching deliver accurate answers even for paraphrased queries.                                     |
| **Google ADK Integration** | Uses LiteLLM model wrapper and `Runner` + `InMemorySessionService` to orchestrate Gemini calls.                                    |
| **Smart Intent Router**    | Keyword & pattern scorer classifies if the question is support-related or health-science related when **Auto Detect** is selected. |
| **Fully Tested**           | `pytest` suite (5 green tests) covers scraper, matcher, ADK mock, and route integration.                                           |
| **CI-ready**               | External Vertex-AI calls are monkey-patched in tests so the suite runs offline and deterministically.                              |

---

##  Project Structure

```
nugenomics_ai_assistant/
│
├── app/
│   ├── __init__.py            # Flask app factory
│   ├── routes.py              # Frontend rendering + intent routing
│   ├── templates/
│   │   └── index.html         # Tailwind UI frontend
│   └── agents/
│       ├── faq_agent.py       # FAQ Agent – scraping + semantic matching
│       └── wellness_agent.py  # Genetic Wellness Agent – uses Google ADK
│
├── tests/                     # pytest suite (ADK mock included)
│
├── run.py                     # Entry point: `python run.py`
├── requirements.txt           # Python dependencies
└── README.md                  # ← you're here
```

---

##  Quick Start

```bash
git clone https://github.com/your-handle/nugenomics_ai_assistant.git
cd nugenomics_ai_assistant
python -m venv venv && source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

##  1. Google Credentials

1. Create a Vertex AI service account with the **Vertex AI User** role.
2. Download the JSON key and store it **outside** your repository.
3. Set the environment variable:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/your-key.json
# On Windows CMD:
set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\key.json
```

---

## ▶ 2. Run the App

```bash
python run.py
# Open http://localhost:5000 in your browser
```

---

##  Testing

```bash
pytest -q
```

You should see:

```text
.....
5 passed in 6.3s
```

 ADK network calls are mocked — **no Google billing is incurred** during testing.

---

##  Deployment Notes

* For production with Gunicorn or Uvicorn, point the WSGI entry to `app:create_app`.
* This app **scrapes live HTML** — if the FAQ site structure changes, update `faq_agent.py` selectors.
* Keep the service account JSON file **outside the repo** and use environment variables for config.

---

##  AI Assistance Disclosure
Portions of the scraping logic, semantic matching heuristics, Google ADK integration, and this README were guided with the help of OpenAI’s ChatGPT and Perplexity AI.
These tools assisted with research, code suggestions, and explanations. All code was reviewed and tested by the author.

---

##  License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

## Author

Created and maintained by Dhiya C Jayakumar (www.linkedin.com/in/dhiya-cjayakumar)

For questions or collaboration, feel free to reach out at [dhiya.cjayakumar@gmail.com](mailto:dhiya.cjayakumar@gmail.com)
