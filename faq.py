from flask import Blueprint, request, jsonify
import spacy
import nltk
from nltk.corpus import wordnet as wn
from transformers import pipeline
import random
import torch
from sentence_transformers import SentenceTransformer, util

faq_bp = Blueprint('faq', __name__)

# Download WordNet data
nltk.download('wordnet')

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize T5 paraphrasing model
paraphraser = pipeline("text2text-generation", model="t5-base", tokenizer="t5-base")

# Load a pre-trained Sentence-BERT model for better sentence similarity
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

# Updated FAQ database (intents and responses)
faq_data = {
    "what_is_novanecter": "Novanecter is a leading provider of innovative solutions in the software development.",
    "services_offered": "We offer services like Web Development, App Development, SEO, Graphics Design, and Custom Software Solutions tailored to your business needs.",
    "contact_support": "You can contact support at info@novanectar.co.in or call us at +91 89798 91703.",
    "pricing_details": "For pricing details, visit our website https://novanectar.co.in/ or contact our sales team at +91 89798 91703.",
    "service_warranty": "Novanecter offers a warranty for all services provided, including bug fixes and support for a defined period after project completion. Please contact us for specific terms.",
    "client_onboarding_process": "Our client onboarding process involves understanding your requirements, project scoping, team assignment, and establishing timelines. We guide you every step of the way.",
    "payment_methods": "We accept payments via bank transfers, credit cards, and online payment systems like PayPal. For more details, contact our accounts team at accounts@novanectar.co.in.",
    "project_management_tools": "We use industry-leading project management tools like Jira and Trello to ensure efficient collaboration, timely delivery, and transparent communication.",
    "post_launch_support": "We offer post-launch support, including maintenance and updates, to ensure your solution continues to perform optimally. Contact our support team for more details.",
    "client_testimonials": "Read what our clients say about us on our testimonials page at https://novanectar.co.in/testimonials.",
    "industry_experience": "Novanecter has over a decade of experience serving clients across various industries, including e-commerce, healthcare, finance, and education.",
    "custom_solution_offering": "We specialize in custom software solutions tailored to meet the unique needs of your business. Let us know your requirements, and we'll create a solution just for you.",
    "integrations_supported": "We support integrations with popular tools and platforms like Salesforce, Shopify, Google Analytics, and more.",
    "service_level_agreement": "We provide service level agreements (SLAs) for our clients, ensuring clear expectations on response times and service delivery. Contact us for detailed SLA information.",
    "company_locations": "Our offices are located in Dehradun, India. Please visit our contact page website https://novanectar.co.in/ for more information.",
    "business_hours": "Our business hours during the holidays are from 9 AM to 6 PM, Monday through Friday.",
    "csr_initiatives": "Novanecter is committed to sustainability and engages in initiatives that support education and environmental efforts.",
    "partnerships": "Yes, we are always looking for new business partnerships. Please reach out to our business development team for more information.",
    "job_openings": "Please check our careers page for the latest job openings and application details.",
    "b2b_services": "Yes, we offer enterprise-level solutions and services tailored to the specific needs of businesses across various industries.",
    "contract_terms": "Our enterprise contracts are customized to meet the unique requirements of each client. Contact us for more information.",
    "account_management": "You can update your business account details by logging into your account dashboard or contacting our support team.",
    "invoice_inquiry": "You can download invoices from your account dashboard or request a copy by emailing accounts@novanectar.co.in.",
    "feedback": "You can leave feedback on our website or directly reach out to our customer service team for more personalized feedback."
}

# Updated Sample phrases for intent matching
intent_phrases = {
    "what_is_novanecter": [
        "What is Novanecter?",
        "Tell me about Novanecter.",
        "What does Novanecter do?",
        "Can you explain Novanecter?",
        "Who is Novanecter?",
        "What type of company is Novanecter?",
        "What services does Novanecter provide?"
    ],
    "services_offered": [
        "What services do you offer?",
        "What kind of services do you provide?",
        "What are your service offerings?",
        "Tell me about the services you offer.",
        "What services are available?",
        "Can you describe your services?",
        "What can you do for me?"
    ],
    "contact_support": [
        "How can I contact support?",
        "How do I reach support?",
        "Where can I get help?",
        "I need assistance, how do I contact support?",
        "How can I get in touch with support?",
        "What is the support contact?",
        "How do I get customer support?"
    ],
    "pricing_details": [
        "What are the pricing details?",
        "Tell me about the pricing.",
        "How much does it cost?",
        "What is the price?",
        "Can you share the cost details?",
        "How do I know the price of your services?",
        "What is the cost for your services?"
    ],
    "service_warranty": [
        "What is the service warranty?",
        "Do you offer a warranty for services?",
        "Tell me about the warranty for your services.",
        "Is there any warranty for the services provided?",
        "What does your warranty cover?",
        "How long is the service warranty?"
    ],
    "client_onboarding_process": [
        "What is the client onboarding process?",
        "How do I get started with Novanecter?",
        "What is the process for new clients?",
        "Tell me how the onboarding process works.",
        "How do I become a client?",
        "What are the steps in the onboarding process?"
    ],
    "payment_methods": [
        "What payment methods do you accept?",
        "How can I pay for your services?",
        "What are the available payment options?",
        "What payment methods are supported?",
        "Can I pay through PayPal or credit card?",
        "Which payment methods do you use?"
    ],
    "project_management_tools": [
        "What project management tools do you use?",
        "Which tools do you use for project management?",
        "How do you manage projects?",
        "Tell me about your project management tools.",
        "What tools help you manage projects?",
        "How do you ensure project success?"
    ],
    "post_launch_support": [
        "Do you offer post-launch support?",
        "What kind of support do you provide after launch?",
        "Is there support after the project is completed?",
        "Do you offer maintenance after the launch?",
        "What post-launch services do you offer?",
        "How do you support after the launch?"
    ],
    "client_testimonials": [
        "Where can I find client testimonials?",
        "Can I read feedback from your clients?",
        "What do your clients say about you?",
        "Do you have any client reviews?",
        "Where can I see client testimonials?",
        "What are your client reviews like?"
    ],
    "industry_experience": [
        "What industries do you serve?",
        "Can you tell me about your industry experience?",
        "What industries has Novanecter worked with?",
        "Which industries do you have experience in?",
        "Tell me about the industries you serve.",
        "What types of businesses have you worked with?"
    ],
    "custom_solution_offering": [
        "Do you provide custom solutions?",
        "Can you build a custom solution for my business?",
        "What custom software solutions do you offer?",
        "Tell me about your custom solution offerings.",
        "Can Novanecter create a solution tailored to my needs?",
        "Do you offer bespoke software solutions?"
    ],
    "integrations_supported": [
        "What integrations do you support?",
        "Which platforms can you integrate with?",
        "Do you support integrations with third-party tools?",
        "What systems can Novanecter integrate with?",
        "Tell me about the integrations you support.",
        "Can you integrate with other software?"
    ],
    "service_level_agreement": [
        "Do you provide service level agreements?",
        "What are your service level agreements?",
        "Can you tell me about your SLAs?",
        "What does your service level agreement cover?",
        "Do you offer SLAs for your services?",
        "What guarantees do you offer in your SLA?"
    ],
    "company_locations": [
        "Where are your offices located?",
        "Where is Novanecter located?",
        "Can you tell me where your headquarters are?",
        "Where can I find your office?",
        "Where is Novanecter based?"
    ],
    "business_hours": [
        "What are your business hours during the holidays?",
        "Are you open during the holidays?",
        "What is your schedule over the holiday season?"
    ],
    "csr_initiatives": [
        "Does your company have any corporate social responsibility initiatives?",
        "What CSR initiatives does Novanecter support?",
        "Can you tell me about your sustainability programs?"
    ],
    "partnerships": [
        "Is the company open to new business partnerships?",
        "Do you collaborate with other companies?",
        "Can I become a partner with Novanecter?"
    ],
    "job_openings": [
        "Do you have any job openings in the marketing department?",
        "Are there any vacancies in your company?",
        "How can I apply for a job at Novanecter?"
    ],
    "b2b_services": [
        "Do you provide services for other businesses?",
        "What B2B services do you offer?",
        "Can you work with other companies?"
    ],
    "contract_terms": [
        "What are the terms of the contract for your enterprise clients?",
        "Can you explain the contract details for large projects?",
        "What does your enterprise contract include?"
    ],
    "account_management": [
        "How can I update my business account details?",
        "How do I manage my account?",
        "Can I change my account information?"
    ],
    "invoice_inquiry": [
        "How do I get a copy of my last invoice?",
        "Can I download my invoice from your website?",
        "How can I view my past invoices?"
    ],
    "feedback": [
        "How can I leave feedback about your services?",
        "Where can I submit feedback?",
        "I want to provide feedback about your services."
    ]
}

# Synonym map (for short queries like "cost")
synonym_map = {
    "cost": "pricing_details",
    "price": "pricing_details",
    "pricing": "pricing_details",
    "support": "contact_support",
    "services": "services_offered",
    "location": "company_locations",
    "feedback": "feedback"
}

# Function to get synonyms using WordNet
def get_synonyms(word):
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)

# Function to augment queries by replacing words with synonyms
def augment_query_with_synonyms(query):
    words = query.split()
    augmented_queries = []
    for word in words:
        synonyms = get_synonyms(word)
        if synonyms:
            new_word = random.choice(synonyms)
            augmented_query = query.replace(word, new_word)
            augmented_queries.append(augmented_query)
    return augmented_queries

# Function to generate paraphrases
def paraphrase_query(query):
    paraphrased_queries = []
    paraphrased = paraphraser(f"paraphrase: {query}", max_length=50, num_return_sequences=3, num_beams=5)
    for p in paraphrased:
        paraphrased_queries.append(p['generated_text'])
    return paraphrased_queries

# Function to augment data
def augment_data(query):
    augmented_with_synonyms = augment_query_with_synonyms(query)
    augmented_with_paraphrasing = paraphrase_query(query)
    all_augmented_queries = list(set(augmented_with_synonyms + augmented_with_paraphrasing))
    return all_augmented_queries

# Improved intent matching using Sentence-BERT for better sentence similarity
def match_intent(user_query):
    # Augment user query with synonyms and paraphrased versions
    augmented_queries = augment_data(user_query)
    
    # Encode user query and augmented queries
    user_query_embedding = sentence_model.encode(user_query, convert_to_tensor=True)
    best_match = None
    highest_similarity = 0.0

    for augmented_query in augmented_queries:
        augmented_query_embedding = sentence_model.encode(augmented_query, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(user_query_embedding, augmented_query_embedding)

        for intent, phrases in intent_phrases.items():
            for phrase in phrases:
                phrase_embedding = sentence_model.encode(phrase, convert_to_tensor=True)
                phrase_similarity = util.pytorch_cos_sim(user_query_embedding, phrase_embedding)

                if phrase_similarity > highest_similarity:
                    highest_similarity = phrase_similarity
                    best_match = intent

    # Fallback mechanism if no match exceeds a certain similarity threshold
    if highest_similarity > 0.6:  # Adjusted threshold for flexible matching
        return best_match
    else:
        return "fallback"

@faq_bp.route('/faq', methods=['POST'])
def faq():
    user_input = request.json.get('query')
    if user_input:
        intent = match_intent(user_input)
        response_text = faq_data.get(intent, "Sorry, I couldn't understand that. Could you please rephrase?")
        return jsonify({"response": response_text})
    return jsonify({"response": "Please provide a query."})
