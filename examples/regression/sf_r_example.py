from simforest import SimilarityForestRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression, load_svmlight_file, load_wine, make_friedman1
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split, GridSearchCV
import numpy as np
from scipy.spatial import distance
import pandas as pd
import matplotlib.pyplot as plt


'''X, y = make_regression(n_features=4, n_informative=4, n_samples=1000, random_state=1)
rng = np.random.RandomState(2)
X += 2 * rng.uniform(size=X.shape)
linearly_separable = (X, y)'''

'''X, y = load_svmlight_file('../data/mpg')
X = X.toarray()'''

#X, y = make_friedman1(n_samples=1000, random_state=42)
#X, y = load_wine(return_X_y=True)


df = pd.read_csv('../data/AirQualityUCI.csv', sep=',')
df.drop(columns=['Date', 'Time', 'AH', 'val1', 'val2', 'val3', 'val4', 'val5'], inplace=True)
df.dropna(inplace=True)
print(df.head())

y, X = df.pop('RH'), df

X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Fit predict for both classifiers
sf = SimilarityForestRegressor(n_estimators=100, criterion='variance')
sf.fit(X_train, y_train)
sf_pred = sf.predict(X_test)
print(f'Similarity Forest R2 score: {r2_score(y_test, sf_pred)}')
print(sf.get_params())


rf = RandomForestRegressor(random_state=42, oob_score=True)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)

# Compare regressors' accuracy
print(f'Random Forest R2 score: {r2_score(y_test, rf_pred)}')

'''# Scale predictions for plotting
sf_pred = (sf_pred - np.min(sf_pred))/np.ptp(sf_pred)
rf_pred = (rf_pred - np.min(rf_pred))/np.ptp(rf_pred)

# Plot classifiers' predictions
plt.scatter(X_test[:, 0], X_test[:, 1], marker='o', c=sf_pred,
            s=50, edgecolor='k', alpha=1.0, cmap='BuPu', lw=0, facecolor='0.5')
plt.title("Similarity Tree")
plt.show()

plt.scatter(X_test[:, 0], X_test[:, 1], marker='o', c=rf_pred,
            s=50, edgecolor='k', alpha=1.0, cmap='BuPu', lw=0, facecolor='0.5')
plt.title("Decision Tree")
plt.show()
plt.scatter(X_test[:, 0], X_test[:, 1], marker='o', c=y_test,
            s=50, edgecolor='k', alpha=1.0, cmap='BuPu', lw=0, facecolor='0.5')
plt.title("True")
plt.show()'''