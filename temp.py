import random
import nltk
from nltk.corpus import wordnet

conversation = {"hello": ["hello", "hey, hello how can i help you"]}

# Define synonyms for common question words
synonyms = {"what": ["what", "which", "where", "when", "how"],
            "is": ["is", "are", "am", "was", "were", "be", "being", "been"]}

# Generate a list of synonyms for a given word using WordNet
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().lower())
    return list(synonyms)

# Check if two words have similar meanings using WordNet
def have_similar_meanings(word1, word2):
    for syn1 in get_synonyms(word1):
        for syn2 in get_synonyms(word2):
            if syn1 == syn2:
                return True
    return False

# Process user input and generate an appropriate response
def respond_to_input(user_input):
    # Check if input matches a conversation keyword
    for key in conversation:
        if user_input.lower() == key:
            return random.choice(conversation[key])
    
    # Check if input is a question
    question_words = synonyms["what"]
    if user_input.lower().startswith(tuple(question_words)):
        # Extract the main verb from the question
        tokens = nltk.word_tokenize(user_input.lower())
        pos_tags = nltk.pos_tag(tokens)
        verbs = [token for token, pos in pos_tags if pos.startswith('V')]
        if len(verbs) > 0:
            main_verb = verbs[0]
            # Check if the main verb has a similar meaning to "is"
            if have_similar_meanings(main_verb, "is"):
                return "I'm not sure, could you please provide more information?"
    
    return "I'm sorry, I don't understand what you're saying."

# Main program loop
while True:
    user_input = input("Say something: ")
    response = respond_to_input(user_input)
    print(response)
