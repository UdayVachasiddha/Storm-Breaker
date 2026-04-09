import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.ensemble import RandomForestClassifier
import warnings

warnings.filterwarnings('ignore')

from ddos_mitigation_simulation import (
    generate_normal_traffic,
    load_and_filter_botnet_data,
    create_hybrid_dataset
)

# Style configuration
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("viridis")
font_options = {'family': 'sans-serif', 'weight': 'bold', 'size': 12}
plt.rc('font', **font_options)

def main():
    print("[*] Creating /research_graphs directory...")
    output_dir = "research_graphs"
    os.makedirs(output_dir, exist_ok=True)
    
    print("[*] Extracting Data...")
    normal_data = generate_normal_traffic(num_samples=5000)
    malicious_data = load_and_filter_botnet_data(num_samples=5000)
    
    X_scaled, y_labels, scaler = create_hybrid_dataset(normal_data, malicious_data)
    
    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_labels, test_size=0.3, random_state=42)
    
    print("[*] Training Baseline Model...")
    rf_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    rf_model.fit(X_train, y_train)
    
    y_pred = rf_model.predict(X_test)
    y_prob = rf_model.predict_proba(X_test)[:, 1] # Probabilities for the strictly positive class (1)
    
    # =======================================================
    # 1. Confusion Matrix Heatmap
    # =======================================================
    print("[*] Generating Confusion Matrix...")
    cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
    
    plt.figure(figsize=(8, 6))
    ax = sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                     xticklabels=['Predicted Normal', 'Predicted Attack'],
                     yticklabels=['Actual Normal', 'Actual Attack'],
                     annot_kws={"size": 16, "weight": "bold"})
    
    plt.title('DDoS Detection Confusion Matrix', fontsize=18, pad=20)
    plt.ylabel('Ground Truth', fontsize=14)
    plt.xlabel('AI Prediction', fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'confusion_matrix.png'), dpi=300)
    plt.close()
    
    # =======================================================
    # 2. Feature Importance Chart
    # =======================================================
    print("[*] Generating Feature Importance Chart...")
    importances = rf_model.feature_importances_
    features = X_train.columns
    
    # Sort them
    indices = np.argsort(importances)[::-1]
    sorted_features = [features[i] for i in indices]
    sorted_importances = importances[indices]
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=sorted_importances, y=sorted_features, palette='mako')
    plt.title('Feature Importance in Attack Detection', fontsize=18, pad=20)
    plt.xlabel('Relative Importance (Gini Impurity Drop)', fontsize=14)
    plt.ylabel('Network Feature', fontsize=14)
    
    # Add exact percentages to bars
    for i, v in enumerate(sorted_importances):
        plt.text(v + 0.01, i, f'{v*100:.1f}%', color='black', va='center', fontweight='bold')
        
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'feature_importance.png'), dpi=300)
    plt.close()
    
    # =======================================================
    # 3. ROC / AUC Curve
    # =======================================================
    print("[*] Generating ROC/AUC Curve...")
    fpr, tpr, thresholds = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(8, 8))
    plt.plot(fpr, tpr, color='darkorange', lw=3, label=f'ROC curve (AUC = {roc_auc:.4f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
    
    plt.xlim([-0.01, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=14)
    plt.ylabel('True Positive Rate', fontsize=14)
    plt.title('Receiver Operating Characteristic (ROC)', fontsize=18, pad=20)
    plt.legend(loc="lower right", fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'roc_curve.png'), dpi=300)
    plt.close()
    
    print(f"\n[+] Success! All publication-ready charts have been saved to '{output_dir}/'.")

if __name__ == "__main__":
    main()
