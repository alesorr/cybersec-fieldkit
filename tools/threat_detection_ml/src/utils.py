import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif

def load_dataset(path):
    """
    Carica il dataset CSV.
    """
    return pd.read_csv(path)

def preprocess_data(df, label_column='Label'):
    """
    Preprocessing dei dati per task multi-class:
    - Rimozione dei valori nulli
    - Encoding delle classi (multi-class)
    - Normalizzazione delle feature
    """
    # Rimozione NaN
    df = df.dropna()

    # Rimuove colonne irrilevanti se presenti
    drop_cols = [col for col in ['Flow ID', 'Source IP', 'Destination IP', 'Timestamp'] if col in df.columns]
    df = df.drop(columns=drop_cols, errors='ignore')

    # Encoding delle etichette multi-classe
    le = LabelEncoder()
    df[label_column] = le.fit_transform(df[label_column])

    # Separazione feature/target
    X = df.drop(columns=[label_column])
    y = df[label_column]

    # Normalizzazione
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler, le

def select_features(X, y, k=20):
    """
    Selezione delle k migliori feature tramite ANOVA F-test.
    """
    selector = SelectKBest(score_func=f_classif, k=k)
    X_selected = selector.fit_transform(X, y)
    return X_selected, selector
