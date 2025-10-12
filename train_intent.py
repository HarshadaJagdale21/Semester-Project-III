import json, os, random, joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

ROOT = os.path.dirname(__file__)
MODEL_DIR = os.path.join(ROOT, "models")
os.makedirs(MODEL_DIR, exist_ok=True)
MODEL_PATH = os.path.join(MODEL_DIR, "intent_model.pkl")

# Load data
with open("intents.json", "r") as f:
    data = json.load(f)

X, y = [], []
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        X.append(pattern)
        y.append(intent["tag"])

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = Pipeline([
    ("vect", CountVectorizer()),
    ("tfidf", TfidfTransformer()),
    ("clf", MultinomialNB())
])
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("Model accuracy:", accuracy_score(y_test, y_pred))
joblib.dump(model, MODEL_PATH)
print("✅ Model saved to:", MODEL_PATH)
