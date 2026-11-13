from pathlib import Path
import pandas as pd
from sklearn.preprocessing import StandardScaler

#base path set
folder = Path(__file__).parent


df = pd.read_excel(folder / "Scenario 2 Dataset.xlsx", keep_default_na=False, na_values=[""])
print("Original shape:", df.shape)

#variables selected 
features = ["Initial_days", "Additional_charges", "Age"]
X = df[features]

#cleaning, checking for missing values and duplicates
print("\nMissing values:\n", X.isna().sum())
print("\nDuplicate rows in full dataset:", df.duplicated().sum())

#different scales of each variable
print("\nSummary before scaling:")
print(X.describe().round(2))

#correlation check
print("\nCorrelation matrix:")
print(df[features + ["TotalCharge"]].corr().round(2))

# each variable has a mean of 0 and a standard deviation of 1
scaler = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=features)

print("\nSummary after scaling:")
print(X_scaled.describe().round(2))


X_scaled.to_csv(folder / "data_ready.csv", index=False)
print("\nSaved")