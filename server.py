import asyncio
import json
import random
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sse_starlette.sse import EventSourceResponse
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix

from whatsapp import send_ddos_alert

from ddos_mitigation_simulation import (
    generate_normal_traffic,
    load_and_filter_botnet_data,
    create_hybrid_dataset
)

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global variables to hold model state
GLOBAL_MODEL = None
GLOBAL_SCALER = None

@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("static/index.html", "r") as f:
        return f.read()

@app.post("/api/train")
async def train_model():
    global GLOBAL_MODEL, GLOBAL_SCALER
    
    # Generate balanced dataset for demo
    normal_data = generate_normal_traffic(num_samples=2500)
    malicious_data = load_and_filter_botnet_data(num_samples=2500)
    
    # Hybrid pipeline
    X, y, trained_scaler = create_hybrid_dataset(normal_data, malicious_data)
    
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    rf_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    rf_model.fit(X_train, y_train)
    
    predictions = rf_model.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    cm = confusion_matrix(y_test, predictions)
    tn, fp, fn, tp = cm.ravel()
    fpr = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0
    
    # Update globals so the simulate endpoint can use them
    GLOBAL_MODEL = rf_model
    GLOBAL_SCALER = trained_scaler
    
    return {
        "status": "success",
        "accuracy": float(acc),
        "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
        "fpr": fpr
    }

@app.get("/api/simulate")
async def simulate_traffic_stream(target_node: str = "ALL"):
    """
    Endpoint that streams Server-Sent Events showing the edge mitigation.
    Accepts target_node to selectively filter Anycast routing.
    """
    global GLOBAL_MODEL, GLOBAL_SCALER
    
    if GLOBAL_MODEL is None or GLOBAL_SCALER is None:
        return {"error": "Model not trained yet."}

    async def event_generator():
        # Increased samples so single-node filtering still has enough traffic to trigger WhatsApp
        stream_samples = 150
        normal_stream = generate_normal_traffic(num_samples=stream_samples // 2)
        malicious_stream = load_and_filter_botnet_data(num_samples=stream_samples - (stream_samples // 2))
        
        mixed_stream = pd.concat([normal_stream, malicious_stream], ignore_index=True)
        mixed_stream = mixed_stream.sample(frac=1).reset_index(drop=True)
        
        features = mixed_stream.drop('label', axis=1)
        true_labels = mixed_stream['label']
        
        dropped_count = 0
        passed_count = 0
        alert_sent = False
        
        # Anycast simulated edge pools
        anycast_nodes = ["BOM-Edge", "FRA-Edge", "TYO-Edge", "SGP-Edge"]
        
        for i in range(len(features)):
            # Randomly simulate Anycast distribution based on presumed geography
            assigned_node = random.choices(anycast_nodes, weights=[0.4, 0.25, 0.2, 0.15])[0]
            
            # If user wants to simulate being a specific node (e.g., BOM-Edge), skip packets routed elsewhere
            if target_node != "ALL" and assigned_node != target_node:
                # Fast forward time mentally; this packet hit a different global datacenter.
                continue
                
            packet_features = GLOBAL_SCALER.transform([features.iloc[i].values])
            prediction = GLOBAL_MODEL.predict(packet_features)[0]
            actual = int(true_labels.iloc[i])
            
            packet_data = {
                "id": i+1,
                "node": assigned_node,
                "packet_size": round(float(features.iloc[i]['packet_size']), 2),
                "inter_arrival_time": round(float(features.iloc[i]['inter_arrival_time_ms']), 2),
                "entropy": round(float(features.iloc[i]['entropy']), 2),
                "variance": round(float(features.iloc[i]['variance']), 2),
                "actual_label": actual,
                "predicted": int(prediction)
            }
            
            if int(prediction) == 1:
                dropped_count += 1
            else:
                passed_count += 1
                
            # Dynamic DDoS Threshold Alert!
            if dropped_count >= 15 and not alert_sent:
                send_ddos_alert(dropped_packets=dropped_count, passed_packets=passed_count)
                alert_sent = True
            
            yield {"data": json.dumps(packet_data)}
            await asyncio.sleep(0.3) # Control speed of visualizer streaming
            
        yield {"data": json.dumps({"status": "done"})}
            
    return EventSourceResponse(event_generator())

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
