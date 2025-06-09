import joblib
import time
import pandas as pd
import pyshark
import utils

# === Caricamento modello e oggetti ===
clf = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')
selector = joblib.load('selector.pkl')
label_encoder = joblib.load('label_encoder.pkl')

# === Funzione per estrarre feature da pacchetto ===
def extract_features_from_packet(pkt):
    try:
        return {
            'packet_length': int(pkt.length),
            'protocol': 1 if pkt.transport_layer == 'TCP' else 0,
            'src_port': int(pkt[pkt.transport_layer].srcport),
            'dst_port': int(pkt[pkt.transport_layer].dstport),
            # Simula alcune feature mancanti
            'flow_duration': 0,
            'fwd_packet_length_mean': 0,
            'bwd_packet_length_mean': 0
        }
    except Exception as e:
        print(f"⚠️ Errore nel pacchetto: {e}")
        return None

# === Inizia la cattura ===
print("🟢 Monitoring network traffic (multi-class)...")
cap = pyshark.LiveCapture(interface='eth0')  # oppure usa un .pcap con sniff_continuously()

for packet in cap.sniff_continuously(packet_count=100):
    features = extract_features_from_packet(packet)
    if features:
        df = pd.DataFrame([features])

        try:
            X = scaler.transform(df)
            X_selected = selector.transform(X)
            prediction = clf.predict(X_selected)
            label = label_encoder.inverse_transform(prediction)

            # Probabilità
            probs = clf.predict_proba(X_selected)[0]
            top_n = sorted(zip(label_encoder.classes_, probs), key=lambda x: x[1], reverse=True)

            print(f"\n🔎 Prediction: {label[0]}")
            print("📊 Class Probabilities:")
            for lbl, prob in top_n:
                print(f"   {lbl:<20} -> {prob:.3f}")

        except Exception as e:
            print(f"❌ Errore durante la predizione: {e}")

    time.sleep(1)  # Simulazione real-time
