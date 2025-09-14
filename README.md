# 🛡️ Cyber Threat Detection Dashboard

An AI-powered dashboard that helps Security Operations Center (SOC) analysts automatically detect and classify malicious network activity.  
Built with **Machine Learning + Streamlit**, it reduces manual inspection time and improves real-time threat response.

---

## 🚀 Features
- 📂 Upload raw **CSV network logs** (UNSW-NB15 dataset format)  
- 🔮 **Random Forest** model for Safe ✅ vs Unsafe 🚨 detection  
- 🎯 **XGBoost** model for multi-class attack categorization (DoS, Exploits, Reconnaissance, Worms, etc.)  
- 📊 Interactive **analytics dashboard** (pie charts of Safe vs Unsafe and attack distribution)  
- 💾 **Download predictions** as `predictions.csv`  
- ⚡ Instant, no-code insights for SOC analysts  

---

## 🏗️ Tech Stack
- **Environment:** Google Colab, VS Code  
- **Libraries:**  
  - `pandas`, `numpy` → data handling  
  - `scikit-learn` → preprocessing, Random Forest, metrics  
  - `xgboost` → attack categorization  
  - `matplotlib` → visualization  
  - `streamlit` → dashboard UI  
  - `joblib` → saving/loading models  

---

## 📊 Dataset
We used the **[UNSW-NB15 dataset](https://research.unsw.edu.au/projects/unsw-nb15-dataset)**, which contains modern network traffic with both normal logs and multiple types of attacks.  
Key features include:
- `proto` (protocol), `service`, `state`  
- `spkts`, `dpkts`, `sbytes`, `dbytes`  
- `rate`, `dur`, and connection stats  
- `label` → Binary target (0 = Normal, 1 = Attack)  
- `attack_cat` → Multi-class target (DoS, Exploits, Recon, etc.)  

---

## ⚙️ Project Workflow
1. **Data Preparation**  
   - Load training & testing datasets  
   - Drop unused metadata columns (`id`, redundant fields)  
   - Encode categorical features (`proto`, `service`, `state`)  
   - Scale numeric features with `StandardScaler`  

2. **Model Training**  
   - **Random Forest (rf_model.pkl):** Binary Safe/Unsafe detection  
   - **XGBoost (xgb_model.pkl):** Multi-class attack classification  
   - Save preprocessing objects (scalers, encoders)  

3. **Model Validation**  
   - Random Forest: ~87% accuracy, high recall for attacks  
   - XGBoost: ~76% accuracy, balanced precision & recall across attack types  
   - Metrics: Accuracy, Precision, Recall, F1-score, Confusion Matrix  

4. **Deployment**  
   - Integrated into **Streamlit dashboard**  
   - Upload → Preprocessing → Prediction → Visualization  
   - Download predictions for offline analysis  


## 📂 Folder Structure
cyber-threat-dashboard/
│── data/ # Dataset CSVs (train/test)
│── models/ # Saved ML models & encoders (.pkl)
│── notebook/ # Google Colab training notebooks
│── dashboard.py # Streamlit app
│── sample_logs.csv # Example input CSV
│── README.md # Project documentation
|-- requirements.txt

---

## 🎮 How to Run
1. Clone the repo:
   ```bash
   git clone https://github.com/zayed789/threat-detection-dashboard.git
   cd threat-detection-dashboard
Install dependencies:
pip install -r requirements.txt
Run the dashboard:

streamlit run dashboard.py
Upload sample_logs.csv (or UNSW-NB15 logs) and view predictions + analytics.

📈 Results & Impact
Random Forest: 87% accuracy → reliable Safe vs Unsafe detection
XGBoost: 76% accuracy → attack categorization with balanced metrics

Impact:
⏱️ Saves hours of manual log inspection
🧠 Reduces analyst fatigue & missed threats
⚡ Enables faster, more reliable threat response

🔮 Future Work
Real-time log ingestion (streaming data) using LLM'
Explainable AI (feature importance per prediction)
Integration with SIEM tools (Splunk, ELK stack)
