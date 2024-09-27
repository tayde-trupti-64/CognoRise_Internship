import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

# Load the dataset
df = pd.read_csv('D:\Data Analyst\CognoRise_Internship\Task_7\Chicago_Crimes_2001_to_2004.csv')

# Preprocessing
df = df.fillna(df.mean())
scaler = StandardScaler()
df[['latitude', 'longitude', 'x_coordinate', 'y_coordinate']] = scaler.fit_transform(df[['latitude', 'longitude', 'x_coordinate', 'y_coordinate']])

# One-hot encoding for categorical variables
ohe = OneHotEncoder(sparse=False)
df[['date_time', 'primary_type', 'arrest']] = ohe.fit_transform(df[['date_time', 'primary_type', 'arrest']])

# Split data into training and testing sets
X = df.drop('case_number', axis=1)
y = df['case_number']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model selection and hyperparameter tuning
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('rf', RandomForestRegressor())
])

param_grid = {
    'rf__n_estimators': [10, 50, 100],
    'rf__max_depth': [None, 5, 10],
    'rf__min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)

# Model evaluation on testing set
y_pred = grid_search.predict(X_test)
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
print("R-Squared Score:", r2_score(y_test, y_pred))





==============================================================================================================================================================================================
==============================================================================================================================================================================================




import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('crimes_in_chicago.csv')

# Check for missing values
print(df.isnull().sum())

# Convert date columns to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Calculate summary statistics
print(df['Primary Type'].value_counts(normalize=True).head(5))
print(df['Community Area'].value_counts(normalize=True).head(5))

# Create a bar chart to show the distribution of crimes by type
plt.figure(figsize=(10,6))
sns.countplot(x='Primary Type', data=df)
plt.title('Distribution of Crimes by Type')
plt.show()

# Create a heatmap to show crime density across neighborhoods
plt.figure(figsize=(10,8))
sns.countplot(x='Community Area', data=df)
plt.title('Crime Density Across Neighborhoods')
plt.show()

# Identify top 5 crime types by frequency
top_crimes = df['Primary Type'].value_counts().head(5)
print(top_crimes)

# Seasonality analysis
df['Month'] = df['Date'].dt.month
monthly_crime_rates = df['Month'].value_counts(normalize=True).sort_index()
plt.figure(figsize=(10,6))
sns.lineplot(x=monthly_crime_rates.index, y=monthly_crime_rates.values)
plt.title('Monthly Crime Rates')
plt.show()

# Heatmap visualization
crime_density = df['Community Area'].value_counts().sort_values(ascending=False)
plt.figure(figsize=(10,8))
sns.heatmap(crime_density.values.reshape(10,10), cmap='coolwarm')
plt.title('Crime Density Heatmap')
plt.show() 