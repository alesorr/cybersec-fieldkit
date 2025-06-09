import pandas as pd
import joblib
import json
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier

import utils

# === Caricamento e preprocessing ===
df = utils.load_dataset('dataset/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv')
X, y, scaler, label_encoder = utils.preprocess_data(df)

# Stampa mapping classi
print("\n🔖 Class index mapping:")
for idx, label in enumerate(label_encoder.classes_):
    print(f"{idx}: {label}")

# === Feature Selection ===
X_selected, selector = utils.select_features(X, y, k=20)

# === Train/test split ===
X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.2, random_state=42)

# === Modelli da testare ===
models = {
    "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
    "GradientBoosting": GradientBoostingClassifier(),
    "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='mlogloss'),
    "LogisticRegression": LogisticRegression(max_iter=1000),
    "KNN": KNeighborsClassifier()
}

# === Addestramento e valutazione ===
reports = {}

for name, model in models.items():
    print(f"\n🧠 Training {name}...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print(f"📊 Classification Report for {name}:")
    report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    print(pd.DataFrame(report).transpose())
    reports[name] = report

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(10, 6))
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=label_encoder.classes_,
                yticklabels=label_encoder.classes_, cmap='Blues')
    plt.title(f'Confusion Matrix - {name}')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.tight_layout()
    plt.savefig(f'confusion_matrix_{name}.png')
    plt.close()

# === Esportazione dei report ===
with open("classification_reports.json", "w") as f:
    json.dump(reports, f, indent=4)

# === Salvataggio del modello preferito (es. RandomForest) ===
joblib.dump(models['RandomForest'], 'model.pkl')
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(selector, 'selector.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')

print("\n✅ Training completato. Modello salvato come 'model.pkl'.")
