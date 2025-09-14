# dashboard.py
import streamlit as st
import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt

# =============================
# Load Models & Preprocessors
# =============================
rf_model = joblib.load("models/rf_model.pkl")
scaler_rf = joblib.load("models/scaler_rf.pkl")

xgb_model = joblib.load("models/xgb_model.pkl")
scaler_mc = joblib.load("models/scaler_mc.pkl")
attack_encoder = joblib.load("models/attack_encoder.pkl")

# =============================
# Page Config
# =============================
st.set_page_config(page_title="🛡️ Cyber Threat Detection", layout="wide")

st.title("🛡️ Cyber Threat Detection Dashboard")
st.markdown("Detect **Safe vs Unsafe** traffic (Random Forest) and classify **attack types** (XGBoost).")

# =============================
# Sidebar Navigation
# =============================
st.sidebar.header("📂 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Upload & Predict", "Analytics"])

# =============================
# Manual Mapping Dictionaries
# =============================
proto_map = {"tcp": 6, "udp": 17, "icmp": 1}
service_map = {"http": 80, "ftp": 21, "dns": 53, "smtp": 25, "ftp-data": 20, "-": 0}
state_map = {"FIN": 0, "INT": 1, "CON": 2, "REQ": 3, "ACC": 4, "RST": 5, "CLO": 6}

# =============================
# Home Page
# =============================
if page == "Home":
    st.subheader("Welcome 👋")
    st.write("""
        This dashboard uses **two ML models** trained on the UNSW-NB15 dataset:
        - 🌱 Random Forest → classifies logs as **Safe / Unsafe**
        - 🔥 XGBoost → detects **attack categories** (DoS, Exploits, Reconnaissance, etc.)

        ### Features:
        - 📂 Upload raw or preprocessed CSVs  
        - 🔮 Get instant predictions (all rows)  
        - 📊 Visualize threat analytics  
        - 💾 Download results  
    """)

# =============================
# Upload & Predict Page
# =============================
elif page == "Upload & Predict":
    st.subheader("📂 Upload CSV for Prediction")

    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"], key="predict_file")

    # ✅ If we already have stored results, show them
    if 'raw_df' in st.session_state and 'predict_df' in st.session_state and uploaded_file is None:
        st.success("✅ Showing last uploaded file and predictions (upload a new file to replace).")
        st.write("### 🔍 Uploaded Data (full):")
        st.dataframe(st.session_state['raw_df'])
        st.write("### 🔮 Predictions:")
        st.dataframe(st.session_state['predict_df'][["proto", "service", "state", "dur", "sbytes", "dbytes", "RF_Prediction", "XGB_Prediction"]])

        # Download button for predictions
        csv_out = st.session_state['predict_df'].to_csv(index=False).encode('utf-8')
        st.download_button("💾 Download Predictions", csv_out, "predictions.csv", "text/csv")

    if uploaded_file is not None:
        raw_df = pd.read_csv(uploaded_file)
        st.session_state['raw_df'] = raw_df.copy()  # ✅ Save original upload

        st.write("### 🔍 Uploaded Data (full):")
        st.dataframe(raw_df)

        # Copy for processing
        df = raw_df.copy()

        # Drop unused columns
        df = df.drop(['id', 'label', 'attack_cat'], axis=1, errors='ignore')

        # ✅ Handle categorical mappings
        if 'proto' in df.columns and df['proto'].dtype == object:
            df['proto'] = df['proto'].map(proto_map).fillna(-1).astype(int)

        if 'service' in df.columns and df['service'].dtype == object:
            df['service'] = df['service'].map(service_map).fillna(-1).astype(int)

        if 'state' in df.columns and df['state'].dtype == object:
            df['state'] = df['state'].map(state_map).fillna(-1).astype(int)

        # ✅ Random Forest
        df_rf = df.drop(['XGB_Prediction', 'RF_Prediction'], axis=1, errors='ignore')
        X_rf = scaler_rf.transform(df_rf)
        rf_preds = rf_model.predict(X_rf)
        df['RF_Prediction'] = np.where(rf_preds == 0, "✅ Safe", "🚨 Unsafe")

        # ✅ XGBoost
        df_mc = df.drop(['XGB_Prediction', 'RF_Prediction'], axis=1, errors='ignore')
        X_mc = scaler_mc.transform(df_mc.values)
        mc_preds = xgb_model.predict(X_mc)
        df['XGB_Prediction'] = attack_encoder.inverse_transform(mc_preds)

        # Save processed df
        st.session_state['predict_df'] = df.copy()

        # Show predictions
        st.success("✅ Predictions complete!")
        st.dataframe(df[["proto", "service", "state", "dur", "sbytes", "dbytes", "RF_Prediction", "XGB_Prediction"]])

        # Download button
        csv_out = df.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Download Predictions", csv_out, "predictions.csv", "text/csv")


# =============================
# Analytics Page
# =============================
elif page == "Analytics":
    st.subheader("📊 Threat Analytics")

    if 'predict_df' in st.session_state:
        df = st.session_state['predict_df']

        # --- Safe vs Unsafe Pie Chart ---
        unsafe_count = (df['RF_Prediction'] == "🚨 Unsafe").sum()
        safe_count = (df['RF_Prediction'] == "✅ Safe").sum()

        st.write(f"✅ Safe: **{safe_count}**")
        st.write(f"🚨 Unsafe: **{unsafe_count}**")

        fig, ax = plt.subplots(figsize=(3, 3))
        ax.pie([safe_count, unsafe_count],
               labels=["Safe", "Unsafe"],
               autopct="%1.1f%%",
               colors=["#4CAF50", "#F44336"])
        ax.set_title("Distribution")
        st.pyplot(fig)

        # --- Attack Categories Bar Chart ---
        if "XGB_Prediction" in df.columns:
            st.write("### 📊 Attack Categories")
            attack_counts = df["XGB_Prediction"].value_counts()
            st.bar_chart(attack_counts)

    else:
        st.warning("⚠️ Please run predictions first in 'Upload & Predict'.")


