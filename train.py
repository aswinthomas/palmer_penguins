import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

# 1. Load the training data
train_df = pd.read_csv('data/train.csv')

# 2. Separate features and target
features = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
target = 'species'
X_train = train_df[features]
y_train = train_df[target]

# 3. Train a simple RandomForest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4. Save the trained model
if not os.path.exists('model'):
    os.makedirs('model')

joblib.dump(model, 'model/model.joblib')

print("Model training complete. penguin_model.joblib saved.")