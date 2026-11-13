from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

folder = Path(__file__).parent

#load from preprocessing
X_scaled = pd.read_csv(folder / "data_ready.csv")
df = pd.read_excel(folder / "Scenario 2 Dataset.xlsx", keep_default_na=False, na_values=[""])
features = ["Initial_days", "Additional_charges", "Age"]

#k = 2 to 10 elbow scores and silhoutte
k_values = range(2, 11)
inertias = []
silhouettes = []
for k in k_values:
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    labels = km.fit_predict(X_scaled)
    inertias.append(km.inertia_)
    silhouettes.append(silhouette_score(X_scaled, labels))

scores = pd.DataFrame({"k": list(k_values),
                       "inertia": [round(i, 1) for i in inertias],
                       "silhouette": [round(s, 4) for s in silhouettes]})
print("Evaluation scores by k:")
print(scores.to_string(index=False))
scores.to_csv(folder / "evaluationscores.csv", index=False)

#elbow plot
plt.figure(figsize=(7, 4))
plt.plot(list(k_values), inertias, marker="o")
plt.title("Elbow Method")
plt.xlabel("Number of clusters")
plt.ylabel("Inertia")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(folder / "elbow.png", dpi=150)
plt.close()

#silhouette plot
plt.figure(figsize=(7, 4))
plt.plot(list(k_values), silhouettes, marker="o", color="darkorange")
plt.title("Silhouette Score by k")
plt.xlabel("Number of clusters")
plt.ylabel("Silhouette score")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(folder / "silhouette.png", dpi=150)
plt.close()

#model with selected number of clusters
final_k = 4
model = KMeans(n_clusters=final_k, n_init=10, random_state=42)
df["Cluster"] = model.fit_predict(X_scaled)
print(f"\nFinal model: k = {final_k}")
print("Silhouette score:", round(silhouette_score(X_scaled, df["Cluster"]), 4))

#cluster assignments 
df[["Customer_id"] + features + ["ReAdmis", "Cluster"]].to_csv(
    folder / "cluster_assignments.csv", index=False)

# Cluster profiles
df["ReAdmissons_flag"] = (df["ReAdmis"] == "Yes").astype(int)
profile = df.groupby("Cluster").agg(
    Patients=("Customer_id", "count"),
    Avg_Initial_days=("Initial_days", "mean"),
    Avg_Additional_charges=("Additional_charges", "mean"),
    Avg_Age=("Age", "mean"),
    Readmission_rate=("ReAdmissons_flag", "mean")
).round(2)
print("\nClusters profiles:")
print(profile.to_string())
profile.to_csv(folder / "clusterprof.csv")

#cluster plot
plt.figure(figsize=(8, 5))
for c in sorted(df["Cluster"].unique()):
    group = df[df["Cluster"] == c]
    plt.scatter(group["Initial_days"], group["Additional_charges"],
                s=8, alpha=0.5, label=f"Cluster {c}")
plt.title("Length of Stay vs. Additional Charges")
plt.xlabel("Initial_days")
plt.ylabel("Additional_charges")
plt.legend(markerscale=3)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(folder / "cluster.png", dpi=150)
plt.close()