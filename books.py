import spacy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from mobi import Mobi
import subprocess

from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation


# Function to extract the text content from a Kindle ebook


def extract_text_from_ebook(file_path):

    # Construct the Calibre CLI command
    command = ['ebook-convert', file_path, 'out.txt']
    # Execute the command and capture the output
    output = subprocess.check_output(command, universal_newlines=True)

    # Open the file in read mode
    with open("out.txt", 'r') as file:
        # Read the contents of the file
        output = file.read()

    # Return the extracted text content
    return output


# Function to update metadata of a Mobi file
def update_metadata(file_path, metadata):
    # Add code to update the metadata of the Mobi file
    pass

# Function to perform Named Entity Recognition (NER)

# Function to perform Named Entity Recognition (NER) with preprocessing


def perform_ner_with_preprocessing(text_content):
    # Preprocess the text content
    # text_content = text_content.lower()  # Convert to lowercase

    # Tokenization
    nlp = spacy.load("en_core_web_sm")
    nlp.max_length = 1500000  # Increase the limit to the desired value

    doc = nlp(text_content)
    tokens = [token.text for token in doc]

    # Remove stop words and punctuation marks
    tokens_without_stopwords = [
        token for token in tokens if token not in STOP_WORDS and token not in punctuation]

    # Perform NER
    processed_text = " ".join(tokens_without_stopwords)
    doc = nlp(processed_text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities


def perform_ner(text_content):
    nlp = spacy.load("en_core_web_sm")
    nlp.max_length = 1500000  # Increase the limit to the desired value

    doc = nlp(text_content)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities


def perform_text_summarization(text_content, num_sentences=3):
    parser = PlaintextParser.from_string(text_content, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary_sentences = summarizer(parser.document, num_sentences)
    summary = " ".join(str(sentence) for sentence in summary_sentences)
    return summary


# Main script
book_file_path = './units/Dune.azw3'

# Extract text content from the Mobi file
text_content = extract_text_from_ebook(book_file_path)
print(f'Extracting text content: {len(text_content)}')
# Update metadata of the Mobi file
metadata = {
    'title': 'New Title',
    'author': 'New Author',
    # Add any other metadata fields you want to update
}
update_metadata(book_file_path, metadata)

# Perform Named Entity Recognition (NER)
ner_entities = perform_ner_with_preprocessing(text_content)

ner_entities = perform_ner(text_content)
print('Named Entities:')
unique_list = list(dict.fromkeys(ner_entities))
print(type(ner_entities), len(ner_entities), len(unique_list))

# Open the file in write mode
with open('unique_list.txt', 'w') as file:
    # Iterate over the list and write each item to a new line in the file
    for item in unique_list:
        file.write(str(item) + '\n')

# for entity in ner_entities:
#     print(entity)

# Perform Text Summarization
# summary = perform_text_summarization(text_content)
# print('Summary:')
# print(summary)
