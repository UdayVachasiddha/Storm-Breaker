import warnings
warnings.filterwarnings('ignore')

from ddos_mitigation_simulation import (
    generate_normal_traffic, 
    load_and_filter_botnet_data, 
    create_hybrid_dataset, 
    train_detection_model
)
import pandas as pd
import numpy as np

print("1. Training the AI Model (with labels)...")
normal_data = generate_normal_traffic(num_samples=2500)
malicious_data = load_and_filter_botnet_data(num_samples=2500)

X_scaled, y_labels, trained_scaler = create_hybrid_dataset(normal_data, malicious_data)
rf_model = train_detection_model(X_scaled, y_labels)

print("\n=======================================================")
print("2. Testing the AI on brand-new, completely UNDECLARED data!")
print("=======================================================\n")

# Let's invent some packets that the AI has NEVER seen, and DO NOT have labels.
# Features: [packet_size, inter_arrival_time_ms, entropy, variance]

unseen_packets = pd.DataFrame({
    'packet_size': [65.0, 1400.0, 60.0, 1250.0],
    'inter_arrival_time_ms': [48.0, 0.01, 52.0, 0.005],
    'entropy': [4.4, 7.8, 4.6, 7.9],
    'variance': [2.1, 950.0, 1.9, 1100.0]
})

print("Here are 4 raw packets arriving at our game server. Notice there is NO label column.")
print(unseen_packets.to_string())
print("\nScaling the packets and feeding them into the AI...")

# Scale features as usual
unseen_scaled = trained_scaler.transform(unseen_packets)

# Predict them - the AI relies ONLY on the 4 features!
predictions = rf_model.predict(unseen_scaled)

print("\n--- AI PREDICTIONS ---")
for i, pred in enumerate(predictions):
    if pred == 0:
        print(f"Packet {i+1}: AI Predicted [0] -> Passed. Looks like a legitimate gamer.")
    else:
        print(f"Packet {i+1}: AI Predicted [1] -> Dropped! Looks like a DDoS Botnet.")
