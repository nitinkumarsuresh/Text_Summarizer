import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from collections import defaultdict

def summarizer(rawdocs):
    stopwords = list(STOP_WORDS)

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(rawdocs)

    # Calculate word frequency using defaultdict
    word_freq = defaultdict(int)
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            word_freq[word.text] += 1

    max_freq = max(word_freq.values())

    # Normalize word frequencies
    for word in word_freq:
        word_freq[word] = word_freq[word] / max_freq

    # Calculate sentence scores considering sentence length
    sent_tokens = [sent for sent in doc.sents]
    sent_scores = {}

    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq:
                if sent not in sent_scores:
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]

        # Normalize by sentence length
        sent_scores[sent] /= len(sent)

    # Select top sentences for summary
    select_len = int(len(sent_tokens) * 0.3)
    summary = nlargest(select_len, sent_scores, key=sent_scores.get)

    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)

    return summary, doc, len(rawdocs.split()), len(summary.split())