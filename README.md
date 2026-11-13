# Patient Segmentation with K-Means Clustering

A k-means clustering analysis that groups 10,000 hospital patients by length of stay, additional charges, and age to support capacity and staffing planning. Built in Python with pandas and scikit-learn as part of the WGU M.S. Data Analytics program.

## Business Problem

The hospital needs to anticipate patient demand to allocate beds and staff more effectively. Length of stay ranges from 1 to 72 days, and the hospital had no clear way to see which groups of patients drive the most bed occupancy and cost. The goal was to segment patients into groups that can be profiled and planned around.

## Data

- Course-provided hospital dataset: 10,000 patients, 50 variables (not included in this repo)
- Variables used for clustering:
  - `Initial_days`: length of stay, the most direct measure of bed occupancy
  - `Additional_charges`: resources used for procedures, treatments, and medications
  - `Age`: patient profile
- `ReAdmis` (readmitted within 30 days) was used only to profile the clusters after they were formed

## Method

1. **Preparation** (`code/preprocessing.py`): checked for missing values and duplicate rows (none found). The three variables were on very different scales (age 18 to 89, stay 1 to 72 days, charges about $3,100 to $30,600), so they were standardized with `StandardScaler` so no single variable dominated the distance calculations.
2. **Model** (`code/clustering.py`): ran k-means for k = 2 through 10 (`n_init=10`, `random_state=42` for reproducibility) and compared each solution with the elbow method and silhouette score.
3. **Selection:** chose **k = 4**. Inertia drops sharply up to k = 4 and flattens after, and the silhouette score rises to 0.415 at k = 4. k = 6 scored slightly higher (0.439) but only split patients into more charge levels without changing the stay or readmission patterns, so the simpler four-cluster solution was kept.

| Elbow Method | Silhouette Score |
|---|---|
| ![Elbow plot](outputs/elbow.png) | ![Silhouette plot](outputs/silhouette.png) |

## Results

![Cluster plot](outputs/cluster.png)

| Cluster | Profile | Patients | Avg. Stay (days) | Avg. Additional Charges | Avg. Age | Readmission Rate |
|---|---|---|---|---|---|---|
| 0 | Short stay, younger, lower cost | 2,682 | 9.2 | $8,390 | 37 | 0% |
| 1 | Long stay, younger, lower cost | 2,601 | 59.7 | $8,454 | 37 | 73% |
| 2 | Short stay, older, higher cost | 2,316 | 9.3 | $18,106 | 72 | 0% |
| 3 | Long stay, older, higher cost | 2,401 | 59.6 | $17,876 | 72 | 74% |

**Key findings**

- **Length of stay is the strongest dividing factor.** The plot shows a clear gap between about 30 and 37 days, splitting short-stay patients (about 9 days) from long-stay patients (about 60 days).
- **Long-stay patients drive bed occupancy.** Clusters 1 and 3 make up half of all patients but account for roughly 87% of total bed days.
- **All readmissions fall in the long-stay clusters**, at 73% and 74%, compared with 0% for short stays.
- **Older patients cost about twice as much** in additional charges, regardless of length of stay.
- **Cluster 3** (long stay, older, higher cost) is the most resource-heavy group.

## Recommendations

1. Build bed capacity and staffing schedules around long-stay demand rather than an average stay.
2. Use the 30-day mark as a checkpoint. Patients still admitted at 30 days are likely in the long-stay group and can be referred for discharge planning and follow-up care to reduce readmissions.
3. Budget more procedure and treatment resources for older patients.

## Limitations

- Length of stay isn't known at admission, so the clusters support overall capacity planning rather than sorting patients on arrival.
- The readmission split (0% vs. 73 to 74%) is unusually clean. Real hospital data is rarely this clear-cut, so findings should be verified against actual records before staffing or budget decisions.

## Repository Structure

```
code/
  preprocessing.py         # missing/duplicate checks, scaling
  clustering.py            # k = 2-10 evaluation, final k = 4 model, profiles, plots
outputs/
  elbow.png                # inertia by k
  silhouette.png           # silhouette score by k
  cluster.png              # length of stay vs. additional charges by cluster
  evaluationscores.csv     # inertia and silhouette for k = 2-10
  clusterprof.csv          # cluster sizes, averages, readmission rates
  preprocessing_output.txt # before/after scaling summaries
  clustering_output.txt    # evaluation scores and cluster profiles
```

## Running It

The dataset was provided through WGU coursework and isn't included here. To reproduce the results, place it in the same folder as the scripts as `Scenario 2 Dataset.xlsx`, then run:

```
pip install pandas scikit-learn matplotlib openpyxl
python preprocessing.py
python clustering.py
```

**Tools:** Python, pandas, scikit-learn, matplotlib
