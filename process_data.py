import pandas as pd
from sklearn.model_selection import train_test_split
import seaborn as sns
import os

# 1. Load the raw dataset
df = sns.load_dataset('penguins')

# 2. Simple data cleaning
df.dropna(inplace=True) # Drop rows with missing values for simplicity
df = df[df['sex'] != '.'] # Remove a row with an invalid value

# 3. Select features and target
features = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
target = 'species'

# 4. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    df[features],
    df[target],
    test_size=0.2,
    random_state=42
)

# 5. Combine features and target for saving
train_data = pd.concat([X_train, y_train], axis=1)
test_data = pd.concat([X_test, y_test], axis=1)

# 6. Save the processed data to local CSV files
if not os.path.exists('data'):
    os.makedirs('data')

train_data.to_csv('data/train.csv', index=False)
test_data.to_csv('data/test.csv', index=False)

print("Data processing complete. train.csv and test.csv created.")