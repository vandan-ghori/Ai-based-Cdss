import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def train():
    # Load data
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'migraine_data.csv')
    print(f"Loading dataset from: {data_path}")
    df = pd.read_csv(data_path)

    # Input features - only 6 selected parameters
    features = ['Age', 'Duration', 'Frequency', 'Intensity', 'Vomit', 'Phonophobia']
    X = df[features]
    y = df['Type']

    # Splitting the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    print("Classification Report:")
    print(classification_report(y_test, predictions))

    # Save the model
    model_path = os.path.join(os.path.dirname(__file__), 'model.joblib')
    joblib.dump(model, model_path)
    print(f"Model saved to: {model_path}")

if __name__ == "__main__":
    train()
