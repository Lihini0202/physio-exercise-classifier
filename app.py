# app.py
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import re

# --- Load Your Model Artifacts ---
# Make sure these .pkl files are in the same folder as app.py
try:
    model = joblib.load("xgb_combined_split.pkl")
    scaler = joblib.load("scaler_combined_split.pkl")
    label_encoder = joblib.load("label_encoder.pkl")
except FileNotFoundError:
    st.error("Model files not found! Make sure 'xgb_combined_split.pkl', 'scaler_combined_split.pkl', and 'label_encoder.pkl' are in the same directory.")
    st.stop()
except Exception as e:
    st.error(f"Error loading model files: {e}")
    st.stop()

# --- Functions from Your Notebook ---

# Helper function to read the uploaded sensor file
def read_numeric_txt(uploaded_file, delimiter=';'):
    try:
        # Read the file as text and process it
        string_data = uploaded_file.getvalue().decode('utf-8')
        lines = [ln.strip() for ln in string_data.splitlines() if ln.strip()]
        
        if any(c.isalpha() for c in lines[0]):
            lines = lines[1:]  # Skip header if present
            
        rows = [re.split(r'\s*;\s*', ln) for ln in lines]
        df = pd.DataFrame(rows)
        
        # Convert all columns to numeric, handling different decimal separators
        df = df.apply(lambda col: pd.to_numeric(col.astype(str).str.replace(',', '.'), errors='coerce'))
        df = df.dropna(axis=1, how='all').dropna(axis=0, how='all')
        
        return df.values
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None

# Your feature extraction function
def extract_features(segments):
    features = []
    for seg in segments:
        mean = np.mean(seg, axis=0)
        std = np.std(seg, axis=0)
        max_val = np.max(seg, axis=0)
        min_val = np.min(seg, axis=0)
        range_val = max_val - min_val
        # Ensure consistent FFT output length
        fft_complex = np.fft.fft(seg, axis=0)
        fft_real = np.abs(fft_complex)[:10].flatten()
        
        # Pad FFT features if segment has fewer than 9 channels (shouldn't happen with 9)
        # We expect 10 FFT components * 9 channels = 90 features
        if len(fft_real) < 90:
            fft_real = np.pad(fft_real, (0, 90 - len(fft_real)))
        
        feat = np.concatenate([mean, std, max_val, min_val, range_val, fft_real])
        features.append(feat)
    return np.array(features)

# --- Streamlit App Interface ---
st.set_page_config(page_title="Physio Exercise Predictor", layout="wide")
st.title("🏃‍♂️ Physiotherapy Exercise Predictor (MLOps Demo)")

st.write("""
Upload a CSV or TXT file of your sensor data (200 rows x 9 channels, semi-colon delimited)
to predict the exercise type.
""")

uploaded_file = st.file_uploader("Choose a sensor data file...", type=["txt", "csv"])

if uploaded_file is not None:
    # 1. Read and Process the Data
    st.info("File uploaded! Processing...")
    sensor_data = read_numeric_txt(uploaded_file)
    
    if sensor_data is not None:
        if sensor_data.shape == (200, 9):
            st.success(f"File read successfully! Shape: {sensor_data.shape}")
            
            # 2. Extract Features
            # We wrap it in a list because extract_features expects a list of segments
            features = extract_features([sensor_data])
            st.write(f"Features extracted. Shape: {features.shape}") # Should be (1, 135)
            
            # 3. Scale Features
            scaled_features = scaler.transform(features)
            
            # 4. Make Prediction
            prediction_proba = model.predict_proba(scaled_features)
            prediction_index = np.argmax(prediction_proba)
            prediction_label = label_encoder.inverse_transform([prediction_index])[0]
            confidence = prediction_proba[0, prediction_index]
            
            # 5. Display Result
            st.subheader("Prediction Result:")
            st.metric(label="Predicted Exercise", value=str(prediction_label), delta=f"{confidence*100:.2f}% Confidence")
            
            # Show confidence for top 5 classes
            st.subheader("Top 5 Predictions:")
            top_5_indices = np.argsort(prediction_proba[0])[::-1][:5]
            top_5_labels = label_encoder.inverse_transform(top_5_indices)
            top_5_probs = prediction_proba[0, top_5_indices]
            
            chart_data = pd.DataFrame({
                "Exercise": top_5_labels,
                "Confidence": top_5_probs
            })
            st.bar_chart(chart_data, x="Exercise", y="Confidence")

        else:
            st.error(f"Error: Uploaded file has the wrong shape! Expected (200, 9) but got {sensor_data.shape}.")