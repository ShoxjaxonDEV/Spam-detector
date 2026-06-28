from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import pandas as pd
import joblib

data = pd.read_csv('spam_ham_dataset.csv', encoding='latin-1', index_col=0)
# print(data.head())
# print(data.columns)
data['label'] = data['label'].fillna(0)
# print(data['label'].value_counts()) #показывает сколько spam, ham
vector = TfidfVectorizer(
    stop_words="english",
    max_features=5000,
    ngram_range=(1, 2),
    min_df=2
)
X = vector.fit_transform(data["text"])
y = data["label"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model = LogisticRegression(max_iter=5000, class_weight="balanced")
# model = MultinomialNB(alpha=0.1)
# model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

feature_names = vector.get_feature_names_out()
# coef = model.coef_[0]
# words_df = pd.DataFrame({
#     'word': feature_names,
#     'weight': coef
# })
pred = model.predict(X_test)
# print(pred)
print("Accuracy:", accuracy_score(y_test, pred))
# print(model.predict_proba(X_test)[:, 1])
print(confusion_matrix(y_test, pred))
# print(classification_report(y_test, pred))
# # print(model.classes_)
# print(words_df.sort_values(by='weight').head(3))
# print(words_df.sort_values(by='weight').tail(3))

# joblib.dump(model, "spam_model_n1.pkl")
# joblib.dump(vector, "vector.pkl")