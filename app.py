import pandas as pd
from difflib import SequenceMatcher
import itertools

# Dictionary of legal terms and their meanings
law_terms = {
    "contravenes": "violates or goes against",
    "abatement": "the reduction or elimination of a nuisance",
    "affiliation": "the state of being closely associated with a particular organization",
    "solemnized": "celebrated with formal ceremony",
    "capitation fee": "a fee or payment of a uniform amount per person",
    "accreditation": "the process of certifying that an institution meets certain standards",
    "commencement": "the beginning or start",
    "cognizance": "awareness or knowledge of something",
    "proficiency": "a high degree of competence or skill",
    "sepulture": "the act of burial",
    "endeavour": "an attempt to achieve a goal",
    "nurse-midwives": "nurses who are trained to deliver babies",
    "waqf": "a religious endowment in Islamic law",
    "deployed": "moved into position for military action",
    "perpetual": "never ending or changing",
    "untenable": "not able to be maintained or defended against attack or objection",
    "decennial": "recurring every ten years",
    "aggrieved": "feeling resentment at having been unfairly treated",
    "pendency": "the state of being pending or awaiting a decision",
    "census": "an official count or survey of a population",
    "contrary": "opposite in nature, direction, or meaning",
    "illegitimate": "not authorized by the law; not in accordance with accepted standards or rules",
    "adherence": "faithful attachment",
    "contract": "a written or spoken agreement that is enforceable by law",
    "expelled": "driven out; forced to leave",
    "pursuance": "the act of pursuing or striving for something",
    "communal": "shared by all members of a community",
    "gazette": "a journal or newspaper, especially an official one",
    "magistrate": "a civil officer who administers the law",
    "sanctity": "the state or quality of being holy, sacred, or saintly",
    "alia": "others (used to indicate other names not mentioned)",
    "forfeiture": "the loss or giving up of something as a penalty for wrongdoing",
    "intestacy": "the condition of dying without a legal will",
    "complies": "acts in accordance with a wish or command",
    "devolve": "transfer or delegate power to a lower level",
    "codicil": "an addition or supplement that explains, modifies, or revokes a will or part of one",
    "appeal": "a request for a higher court to review the decision of a lower court",
    "intestate": "a person who has died without having made a will",
    "cessation": "the fact or process of ending or being brought to an end",
    "norms": "standards of proper or acceptable behavior",
    "interim": "the intervening time; temporary or provisional",
    "memorandum": "a written message in business or diplomacy",
    "apprentice": "a person who is learning a trade from a skilled employer",
    "nullity": "the state of being legally void",
    "wakf": "see waqf",
    "sue": "to bring a legal action against someone",
    "decree": "an official order issued by a legal authority",
    "sued": "past tense of sue",
    "alimony": "a husband's or wife's court-ordered provision for a spouse after separation or divorce",
    "endowments": "the action of endowing something or someone",
    "endowment": "an income or form of property given or bequeathed to someone",
    "dissemination": "the act of spreading something, especially information, widely",
    "testamentary": "related to or bequeathed or appointed through a will",
    "acquisition": "an asset or object bought or obtained",
    "senate": "the smaller upper assembly in the US Congress, most US states, France, and other countries",
    "paramount": "more important than anything else; supreme",
    "consultation": "the action or process of formally consulting or discussing",
    "syllabi": "plural of syllabus, an outline of the subjects in a course of study or teaching",
    "superintendence": "the act of overseeing or directing",
    "pilgrim": "a person who journeys to a sacred place for religious reasons",
    "conferment": "the act of conferring or bestowing (an honor, right, or gift)",
    "de facto": "in fact, whether by right or not",
    "coercion": "the practice of persuading someone to do something by using force or threats",
    "ordinance": "a piece of legislation enacted by a municipal authority",
    "consummate": "make (a marriage or relationship) complete by having sexual intercourse",
    "consolidated": "combined into a single, more effective or coherent whole",
    "contravention": "an action which offends against a law, treaty, or other ruling",
    "solemnization": "the performance of a ceremony (such as a marriage)",
    "infringement": "the action of breaking the terms of a law, agreement, etc.; violation",
    "vocational": "relating to an occupation or employment",
    "fornication": "sexual intercourse between people not married to each other",
    "marginalize": "treat (a person, group, or concept) as insignificant or peripheral",
    "bigamy": "the act of going through a marriage ceremony while already married to another person",
    "cornerstone": "an important quality or feature on which a particular thing depends or is based",
    "adequate": "satisfactory or acceptable in quality or quantity",
    "apprehension": "anxiety or fear that something bad or unpleasant will happen",
    "compliance": "the action or fact of complying with a wish or command",
    "accredit": "give credit to (someone) for something",
    "tribunal": "a body established to settle certain types of dispute",
    "psychotropic": "relating to or denoting drugs that affect a person's mental state",
    "ostensible": "stated or appearing to be true, but not necessarily so",
    "ammunition": "a supply or quantity of bullets and shells",
    "affiliated": "officially attached or connected to an organization",
    "subsistence": "the action or fact of maintaining or supporting oneself, especially at a minimal level",
    "thereto": "to that or to this",
    "therewith": "with that or this",
    "abolition": "the action or an act of abolishing a system, practice, or institution",
    "curb": "restrain or keep in check",
    "regime": "a government, especially an authoritarian one"
}

def replace_words(sentence, replacements):
    words = sentence.split()
    replaced_sentences = []

    for comb in range(1, len(replacements) + 1):
        for subset in itertools.combinations(replacements.keys(), comb):
            new_sentence = []
            for word in words:
                if word in subset:
                    new_sentence.append(replacements[word])
                else:
                    new_sentence.append(word)
            replaced_sentences.append(' '.join(new_sentence))

    return replaced_sentences

def generate_sentence_variations(sentence, terms_dict):
    words = sentence.split()
    terms_in_sentence = {word: terms_dict[word] for word in words if word in terms_dict}

    if not terms_in_sentence:
        return [sentence]

    replaced_sentences = replace_words(sentence, terms_in_sentence)

    return [sentence] + replaced_sentences

def get_sentence_variations(sentence):
    variations = generate_sentence_variations(sentence, law_terms)
    return variations

def remove_words(sentence):
    words_to_remove = {'is', 'and', 'are', 'on', 'of', 'to', 'am', 'when', 'for', 'while', 'where', 'this'}
    words = sentence.split()
    filtered_words = [word for word in words if word.lower() not in words_to_remove]
    return ' '.join(filtered_words)

def string_similarity(word1, word2):
    ratio = SequenceMatcher(None, word1, word2).ratio()
    return ratio >= 0.50

def sentence_similarity(sentence1, sentence2):
    sen1 = sentence1.split()
    sen2 = sentence2.split()
    total = len(sen1) + len(sen2)
    count = 0
    for word1 in sen1:
        for word2 in sen2:
            if string_similarity(word1, word2):
                count += 1
    r1 = count / len(sen1)
    r2 = count / len(sen2)
    return r1 >= 0.25 or r2 >= 0.25

def generate_google_search_link(jurisdictional_reference):
    query = jurisdictional_reference.replace(" ", "+")
    return f"https://www.google.com/search?q={query}"

# Load the CSV file into a DataFrame with a specified encoding
file_path = 'dataset.csv'
try:
    df = pd.read_csv(file_path, encoding='latin1')  # You can also try 'ISO-8859-1' if 'latin1' doesn't work
except UnicodeDecodeError as e:
    print(f"Error reading the CSV file: {e}")
    exit()

# Check if the required columns are in the DataFrame
required_columns = ['Type', 'Description', 'Jurisdictional Reference']
if not all(col in df.columns for col in required_columns):
    print("The CSV file must contain 'Type', 'Description', and 'Jurisdictional Reference' columns.")
    exit()

results = []

while True:
    # Take user input for the type of law
    law_type = input("Enter the type of law (or 'exit' to quit): ").strip().lower()
    if law_type == 'exit':
        break

    # Filter the DataFrame based on user input
    filtered_df = df[df['Type'].str.lower() == law_type]

    # Check if there are any matching rows
    if filtered_df.empty:
        print("No matching laws found.")
    else:
        print("Matching rows found:")
        description_list = filtered_df['Description'].tolist()
        case = input("Enter the case details in one sentence: ").strip()
        case1 = remove_words(case)

        ll = []
        for ss in description_list:
            variations = get_sentence_variations(ss)
            for variation in variations:
                rss = remove_words(variation)
                if sentence_similarity(rss, case1):
                    ll.append(ss)
                    break

        if len(ll) == 0:
            print("No similar laws found.")
        else:
            index = 0
            batch_size = 5
            while index < len(ll):
                solution = filtered_df[filtered_df['Description'].isin(ll)]
                # Assuming there's a column containing jurisdictional references, select that column for Google search links
                reference_column = solution.columns[solution.columns.str.contains('Reference', case=False)].tolist()
                if reference_column:
                    solution['Google Search Link'] = solution[reference_column[0]].apply(generate_google_search_link)
                results.extend(solution.to_dict('records'))
                print(solution)
                output_file_path = '/content/output.csv'
                output_df = pd.DataFrame(results)
                output_df.to_csv(output_file_path, index=False, encoding='utf-8')
                print(f"Results saved to {output_file_path}")
                index += batch_size
                if index < len(ll):
                    cont = input("Do you want to see more laws? (yes/no): ").strip().lower()
                    if cont != 'yes':
                        break

    continue_input = input("Do you want to enter another case? (yes/no): ").strip().lower()
    if continue_input != 'yes':
        break

# Save results to a CSV file
output_file_path = '/content/output.csv'
output_df = pd.DataFrame(results)
output_df.to_csv(output_file_path, index=False, encoding='utf-8')
print(f"Results saved to {output_file_path}")
