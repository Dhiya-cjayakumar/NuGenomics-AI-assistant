import requests
from bs4 import BeautifulSoup
import difflib

FAQ_URL = "https://www.nugenomics.in/faqs/"

def scrape_faq():
    try:
        response = requests.get(FAQ_URL, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching FAQ page: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    faq_list = []

    # Loop through all <h4> tags (questions)
    for question_tag in soup.find_all("h4"):
        question = question_tag.get_text(strip=True)
        # Find the next <div> sibling that contains the answer
        answer_tag = question_tag.find_next_sibling("div")
        answer = answer_tag.get_text(strip=True) if answer_tag else ""
        if question and answer:
            faq_list.append({"question": question, "answer": answer})

    return faq_list

def find_best_answer(query):
    """
    Improved FAQ matching algorithm with semantic understanding
    """
    faq_data = scrape_faq()
    
    if not faq_data:
        return "Sorry, I couldn't load the FAQ data. Please try again later."
    
    query_lower = query.strip().lower()
    
    # Define semantic keyword groups for better matching
    semantic_groups = {
        'timing_blood_report': {
            'keywords': ['when', 'blood', 'report', 'ready', 'time', 'receive', 'get'],
            'phrases': ['blood report', 'get my blood', 'when will i get'],
            'target_question_keywords': ['when', 'blood', 'report']
        },
        'payment_cost': {
            'keywords': ['paid', 'cost', 'price', 'pay', 'money', 'expensive', 'free', 'charge'],
            'phrases': ['is paid', 'program paid', 'cost of', 'how much'],
            'target_question_keywords': ['pay', 'emi', 'cost', 'price']
        },
        'program_duration': {
            'keywords': ['long', 'duration', 'months', 'weeks', 'time', 'last', 'how long'],
            'phrases': ['how long', 'program last', 'duration of'],
            'target_question_keywords': ['long', 'last', 'months', 'usually']
        },
        'gym_exercise': {
            'keywords': ['gym', 'exercise', 'workout', 'fitness', 'membership'],
            'phrases': ['gym membership', 'need gym'],
            'target_question_keywords': ['gym', 'membership', 'exercise']
        },
        'reschedule': {
            'keywords': ['reschedule', 'change', 'postpone', 'appointment', 'session'],
            'phrases': ['reschedule session', 'change appointment'],
            'target_question_keywords': ['reschedule', 'session', 'counselling']
        },
        'program_info': {
            'keywords': ['what', 'program', 'nugenomics', 'about'],
            'phrases': ['what is', 'about program'],
            'target_question_keywords': ['who', 'program', 'for']
        },
        'how_it_works': {
            'keywords': ['how', 'work', 'works', 'process'],
            'phrases': ['how does', 'how it works'],
            'target_question_keywords': ['how', 'does', 'work']
        },
        'sample_collection': {
            'keywords': ['sample', 'collection', 'reschedule', 'collect'],
            'phrases': ['sample collection', 'reschedule sample'],
            'target_question_keywords': ['sample', 'collection', 'reschedule']
        }
    }
    
    # Step 1: Check for semantic group matches
    for group_name, group_data in semantic_groups.items():
        # Check if query matches this semantic group
        query_matches_group = False
        
        # Check for phrase matches first (highest priority)
        for phrase in group_data['phrases']:
            if phrase in query_lower:
                query_matches_group = True
                break
        
        # Check for keyword matches (need at least 2 keywords to match)
        if not query_matches_group:
            matched_keywords = [kw for kw in group_data['keywords'] if kw in query_lower]
            if len(matched_keywords) >= 2:
                query_matches_group = True
        
        if query_matches_group:
            # Find the FAQ that best matches this semantic group
            best_score = 0
            best_match = None
            
            for item in faq_data:
                question_lower = item["question"].lower()
                score = 0
                
                # Count matches with target question keywords
                for target_kw in group_data['target_question_keywords']:
                    if target_kw in question_lower:
                        score += 5  # High score for target keywords
                
                # Bonus for exact phrase matches in question
                for phrase in group_data['phrases']:
                    if phrase.replace(' ', '') in question_lower.replace(' ', ''):
                        score += 10
                
                if score > best_score:
                    best_score = score
                    best_match = item
            
            if best_match and best_score > 0:
                return best_match["answer"]
    
    # Step 2: Exact phrase matching for multi-word queries
    query_words = [word for word in query_lower.split() if len(word) > 2]
    
    if len(query_words) > 1:
        for item in faq_data:
            question_lower = item["question"].lower()
            # Check for multi-word phrases
            for i in range(len(query_words) - 1):
                phrase = " ".join(query_words[i:i+2])
                if phrase in question_lower:
                    return item["answer"]
    
    # Step 3: Score-based matching
    scored_matches = []
    
    for item in faq_data:
        question_lower = item["question"].lower()
        question_words = set(question_lower.split())
        
        # Count matching words
        matching_words = [word for word in query_words if word in question_words]
        match_score = len(matching_words)
        
        # Bonus points for important keywords
        important_keywords = {
            'blood': 4, 'report': 4, 'when': 3, 'will': 2,
            'paid': 5, 'cost': 5, 'price': 5, 'pay': 5, 'emi': 4,
            'program': 2, 'duration': 4, 'long': 3, 'months': 4,
            'gym': 5, 'exercise': 4, 'fitness': 3, 'membership': 5,
            'reschedule': 5, 'change': 3, 'appointment': 4, 'session': 4
        }
        
        for word in matching_words:
            if word in important_keywords:
                match_score += important_keywords[word]
        
        if match_score > 0:
            scored_matches.append((match_score, item))
    
    # Return the highest scoring match
    if scored_matches:
        scored_matches.sort(key=lambda x: x[0], reverse=True)
        return scored_matches[0][1]["answer"]
    
    # Step 4: Fallback to fuzzy matching
    questions = [item["question"].lower().strip() for item in faq_data]
    match = difflib.get_close_matches(query_lower, questions, n=1, cutoff=0.3)
    
    if match:
        for item in faq_data:
            if item["question"].lower().strip() == match[0]:
                return item["answer"]
    
    return "Sorry, I couldn't find an answer to your question. Please contact our support team at support@nugenomics.in"

def run(query: str) -> str:
    return find_best_answer(query)

# Debug function to test scraping
'''def debug_scraping():
    """Debug function to test scraping - remove after testing"""
    faq_data = scrape_faq()
    print(f"Total FAQs scraped: {len(faq_data)}")
    for i, item in enumerate(faq_data[:5]):  # Show first 5
        print(f"{i+1}. Q: {item['question']}")
        print(f"   A: {item['answer'][:80]}...")
    return faq_data

# Test specific queries
def test_queries():
    """Test function for specific problematic queries"""
    test_cases = [
        "when will i get my blood report",
        "is this program paid", 
        "how long is the program",
        "do i need gym membership",
        "what is nugenomics"
    ]
    
    for query in test_cases:
        print(f"\nQuery: '{query}'")
        answer = run(query)
        print(f"Answer: {answer[:100]}...")'''

# Optional: remove or comment out this test block before deployment
'''if __name__ == "__main__":
    print("=== FAQ Agent Debug ===")
    debug_scraping()
    print("\n=== Testing Queries ===")
    test_queries()
    
    print("\n=== Interactive Testing ===")
    while True:
        user_query = input("Ask a NuGenomics support question (or type 'exit' to quit): ")
        if user_query.strip().lower() in {"exit", "quit"}:
            break
        answer = run(user_query)
        print(f"\nAnswer:\n{answer}\n")'''