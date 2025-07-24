import re
from app.agents import faq_agent

def test_faq_scraping():
    data = faq_agent.scrape_faq()
    assert len(data) > 10            # Sanity check: should scrape multiple FAQs
    assert all('question' in d and 'answer' in d for d in data)

def test_faq_matching_keywords():
    # Basic query that should match a common phrase on the FAQ page
    answer = faq_agent.run("How long is the program?")
    assert re.search(r"\b3\s*months?\b", answer, flags=re.I)

def test_faq_no_data():
    # Simulate scrape failure returning empty list
    original_scrape = faq_agent.scrape_faq
    faq_agent.scrape_faq = lambda: []
    answer = faq_agent.run("Any question")
    assert "couldn't load the FAQ data" in answer
    faq_agent.scrape_faq = original_scrape  # revert patch
