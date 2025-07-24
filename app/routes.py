from flask import render_template, request, Blueprint
from .agents.faq_agent import run as run_faq
from .agents.wellness_agent import run as run_wellness
import markdown
from markupsafe import Markup

routes = Blueprint('routes', __name__)

def smart_intent_classifier(query):
    """
    Smart intent detection to classify queries as FAQ/Support or Wellness/Genetic
    """
    query_lower = query.lower().strip()
    
    # Define comprehensive keyword categories for FAQ/Support
    faq_support_keywords = {
        'payment': ['paid', 'cost', 'price', 'expensive', 'free', 'payment', 'emi', 'charge', 'fee', 'money', 'pay'],
        'program_logistics': ['program', 'plan', 'duration', 'long', 'time', 'months', 'weeks', 'start', 'when', 'schedule'],
        'support': ['support', 'help', 'customer', 'service', 'contact', 'phone', 'email', 'refund', 'cancel'],
        'process': ['sample', 'blood', 'report', 'test', 'kit', 'saliva', 'collection', 'results', 'ready'],
        'requirements': ['gym', 'exercise', 'equipment', 'membership', 'need', 'required', 'necessary'],
        'eligibility': ['eligible', 'age', 'pregnant', 'pregnancy', 'condition', 'medical', 'suitable'],
        'booking': ['book', 'appointment', 'reschedule', 'change', 'slot', 'available']
    }
    
    # Define keywords for Wellness/Genetic queries
    wellness_genetic_keywords = {
        'genetics': ['dna', 'gene', 'genetic', 'genome', 'chromosome', 'allele', 'mutation', 'hereditary'],
        'health': ['health', 'wellness', 'fitness', 'nutrition', 'diet', 'metabolism', 'immunity'],
        'conditions': ['diabetes', 'obesity', 'heart', 'disease', 'condition', 'risk', 'predisposition'],
        'lifestyle': ['exercise', 'workout', 'food', 'supplement', 'vitamin', 'mineral', 'lifestyle'],
        'science': ['research', 'study', 'science', 'how', 'why', 'what', 'explain', 'mechanism']
    }
    
    # Calculate FAQ/Support score
    faq_score = 0
    for category, keywords in faq_support_keywords.items():
        for keyword in keywords:
            if keyword in query_lower:
                faq_score += 1
    
    # Calculate Wellness/Genetic score
    wellness_score = 0
    for category, keywords in wellness_genetic_keywords.items():
        for keyword in keywords:
            if keyword in query_lower:
                wellness_score += 1
    
    # Check for FAQ patterns (higher weight)
    faq_patterns = [
        'how much', 'how long', 'when will', 'do i have to', 'is this',
        'can i', 'what do i need', 'where do i', 'how do i pay',
        'what is the cost', 'is it free', 'do you have'
    ]
    
    for pattern in faq_patterns:
        if pattern in query_lower:
            faq_score += 2  # Higher weight for patterns
    
    # Check for Wellness patterns (higher weight)
    wellness_patterns = [
        'how does', 'what role does', 'how do genes', 'what are the effects',
        'how can genetics', 'what causes', 'how genetics affect', 'genetic influence'
    ]
    
    for pattern in wellness_patterns:
        if pattern in query_lower:
            wellness_score += 2  # Higher weight for patterns
    
    # Classification decision
    if faq_score > wellness_score:
        return 'faq'
    elif wellness_score > faq_score:
        return 'wellness'
    else:
        # Tie-breaker: check for clear transactional intent
        transaction_words = ['cost', 'price', 'pay', 'free', 'charge', 'book', 'appointment']
        if any(word in query_lower for word in transaction_words):
            return 'faq'
        else:
            return 'wellness'

@routes.route('/', methods=['GET', 'POST'])
def index():
    response = None
    agent_choice = 'auto'
    user_input = ""

    if request.method == 'POST':
        user_input = request.form.get('query', '').strip()
        agent_choice = request.form.get('agent_choice', 'auto').lower()

        if not user_input:
            response = "Please enter your question."
        elif agent_choice == 'faq':
            response = run_faq(user_input)
        elif agent_choice == 'wellness':
            raw_response = run_wellness(user_input)
            response = Markup(markdown.markdown(raw_response))
        else:
            # 🔥 IMPROVED: Smart auto-detection
            detected_intent = smart_intent_classifier(user_input)
            
            if detected_intent == 'faq':
                response = run_faq(user_input)
                agent_choice = 'faq'
            else:
                raw_response = run_wellness(user_input)
                response = Markup(markdown.markdown(raw_response))
                agent_choice = 'wellness'

    agent_display_name = (
        "Customer Support Agent" if agent_choice == "faq"
        else "Genetic Wellness Info Agent" if agent_choice == "wellness"
        else "Auto Detected Agent"
    )

    return render_template(
        'index.html',
        response=response,
        agent_display_name=agent_display_name,
        selected_agent=agent_choice,
        query=user_input
    )