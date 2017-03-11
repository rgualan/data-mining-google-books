import collection_reader

from sklearn.feature_extraction.text import CountVectorizer


corpus = collection_reader.read_documents()

vectorizer = CountVectorizer(min_df=1)

X = vectorizer.fit_transform(corpus)

print(X)