# import math
# import re
#
# # Read all problem names (each line is a document)
# with open('codechef_name.txt', 'r', encoding='utf-8') as f:
#     lines = [line.strip().lower() for line in f if line.strip()]
#
# # Tokenize words using regex (case-insensitive, alphanumeric only)
# docs = [set(re.findall(r'\b\w+\b', line)) for line in lines]
#
# # Collect all unique words
# word_set = set()
# for doc in docs:
#     word_set.update(doc)
# words = sorted(word_set)  # lexicographical order
#
# # Calculate IDF values
# N = len(docs)
# idf_values = []
# for word in words:
#     doc_count = sum(1 for doc in docs if word in doc)
#     idf = math.log10(N / doc_count)
#     idf_values.append(idf)
#
# # Save words to text file
# with open('codechef_lexicographical_word.txt', 'w', encoding='utf-8') as f:
#     for word in words:
#         f.write(word + '\n')
#
# # Save corresponding IDF values
# with open('codechef_idf.txt', 'w', encoding='utf-8') as f:
#     for val in idf_values:
#         f.write(f"{val:.6f}\n")
import re
from collections import Counter
import math

# Load keywords and IDF
import re
import math
from collections import Counter

# Load keywords and their IDF values
with open('codechef_lexicographical_word.txt', 'r', encoding='utf-8') as f:
    keywords = [line.strip().lower() for line in f if line.strip()]

with open('codechef_idf.txt', 'r', encoding='utf-8') as f:
    idf_values = [float(line.strip()) for line in f if line.strip()]

keyword_index = {word: idx for idx, word in enumerate(keywords)}

# Load all documents (problem names)
with open('codechef_name.txt', 'r', encoding='utf-8') as f:
    docs = [line.strip().lower() for line in f if line.strip()]

# Prepare output files
with open('TFIDF.txt', 'w', encoding='utf-8') as f_tfidf, open('Magnitude.txt', 'w', encoding='utf-8') as f_mag:
    for doc in docs:
        words = re.findall(r'\b\w+\b', doc)
        total = len(words)
        count = Counter(words)

        entries = []
        sum_sq = 0.0

        for word, freq in count.items():
            if word in keyword_index:
                tf = freq / total
                idf = idf_values[keyword_index[word]]
                tfidf = tf * idf
                entries.append((keyword_index[word], tfidf))
                sum_sq += tfidf * tfidf

        # Sort by column index for consistency
        entries.sort()

        # Write TFIDF row
        line = " ".join(f"{col} {val:.6f}" for col, val in entries)
        f_tfidf.write(line + "\n")

        # Write magnitude
        magnitude = math.sqrt(sum_sq)
        f_mag.write(f"{magnitude:.6f}\n")
