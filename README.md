# physio-exercise-classifier
# 🏃‍♂️ Physio Exercise Classifier: An End-to-End MLOps Project

This project demonstrates a complete, end-to-end **MLOps (Machine Learning Operations) pipeline**. It includes a complex **XGBoost model** trained on time-series sensor data from two datasets (UCI and PHYTMO), containerized with Docker, and deployed as a live web app on **Microsoft Azure** using **Terraform**.

The live application is an interactive **Streamlit dashboard** that allows users to upload their own 200x9 sensor data file. The app then runs the full **feature-extraction pipeline**, loads the trained model, and predicts which of the 43 physiotherapy exercises the user is performing.


---

## 🛠️ Core Technologies & DevOps Stack

- **Cloud Provider:** Microsoft Azure  
- **Infrastructure as Code (IaC):** Terraform  
- **Containerization:** Docker  
- **CI/CD:** GitHub Actions (for automated CI) & Manual CD Pipeline  
- **Azure Services:** 
  - `azurerm_resource_group`
  - `azurerm_container_registry` (ACR)
  - `azurerm_container_group` (ACI)  
- **Data Science:** Python, Streamlit, XGBoost, Scikit-learn, Pandas, NumPy  

---

## 🗂️ Project Structure: Two Pipelines in One Repo

This repository contains **two complete pipelines**:

### 1. The ML Training Pipeline (The "Brain")

**File:** `hybrid_physico.ipynb`  

**Purpose:** This Jupyter Notebook is where the model was trained. It performs:

- **Data Ingestion:** Loads and extracts two physiotherapy datasets (UCI and PHYTMO).  
- **Data Preprocessing:** Combines, segments, and resizes 9-channel time-series data into 200-timestep windows.  
- **Feature Extraction:** Generates 135 features from raw sensor data (mean, std, min, max, range, FFT components).  
- **Model Training:** Trains and validates **Random Forest** and **XGBoost Classifier** (82% accuracy) on 90,000+ samples.  
- **Artifact Export:** Saves three essential "model artifacts" for production:  
  - `xgb_combined_split.pkl`  
  - `scaler_combined_split.pkl`  
  - `label_encoder.pkl`  

### 2. The MLOps Deployment Pipeline (The "Factory")

**Files:** `app.py`, `Dockerfile`, `terraform/`, `.github/workflows/`  

**Purpose:** Serves the trained model as a production-ready service.

---

## 🚀 MLOps Deployment Workflow

### 1. Containerization (Docker)
The `Dockerfile` packages the entire **Inference Pipeline** into a portable container, including:  

- Streamlit frontend (`app.py`)  
- Python dependencies (`requirements.txt`)  
- Trained model artifacts (`.pkl` files)  

### 2. Infrastructure as Code (Terraform)
The `/terraform` folder builds all required Azure infrastructure:  

- **Resource Group:** `physio-predictor-rg`  
- **Azure Container Registry (ACR):** Secure storage for Docker images  
- **Azure Container Instance (ACI):** Serverless instance to run the app with a public IP  

### 3. Continuous Integration / Continuous Deployment (CI/CD)

**Continuous Integration (CI):**  
- GitHub Actions (`.github/workflows/ci-pipeline.yml`) runs on every push to main:  
  - Lints code with `flake8`  
  - Scans vulnerabilities with `Trivy`  
  - Tests Docker image build  

**Continuous Deployment (CD):**  
- Deployment is **manual** due to student account restrictions but demonstrates a professional workflow.

---

## ⚙️ Manual Deployment Workflow (Run This Project)

1. **Install Tools & Log In:**  
   ```bash
   az login
   terraform init
````
````
2. **Build the "Cloud Factory"** (initial apply may fail):

   ```bash
   cd terraform
   terraform apply -auto-approve
   ```

3. **Get Your Registry Name:**

   ```bash
   export ACR_NAME=$(terraform output -raw physio_acr_name)
   echo "New registry is: $ACR_NAME"
   ```

4. **Build & Push Docker Image:**

   ```bash
   az acr login --name $ACR_NAME
   cd ..  # Go back to main folder

   # Build the image
   docker build -t $ACR_NAME.azurecr.io/physio-predictor:latest .

   # Push the image
   docker push $ACR_NAME.azurecr.io/physio-predictor:latest
   ```

5. **Deploy Your App (Final Step):**

   ```bash
   cd terraform
   terraform apply -auto-approve
   ```

* After deployment, Terraform outputs the **live app URL**.

---

## 🧹 Clean Up (Save Your Azure Credits)

Destroy all resources when done:

```bash
cd terraform
terraform destroy -auto-approve
```

---

## 📦 Folder Structure

```
physio-exercise-classifier/
│
├─ hybrid_physico (2).ipynb      # ML training notebook
├─ app.py                        # Streamlit inference app
├─ Dockerfile                     # Docker build instructions
├─ requirements.txt               # Python dependencies
├─ terraform/                     # IaC folder
│   ├─ main.tf
│   ├─ variables.tf
│   └─ outputs.tf
└─ .github/workflows/             # CI pipeline
```

---

## 🎯 Key Features

* ✅ End-to-end **ML pipeline** from raw sensor data to prediction
* ✅ **Feature extraction** with FFT, mean, std, min, max, range
* ✅ **XGBoost model** with 82% accuracy
* ✅ **Containerized** using Docker
* ✅ **Azure deployment** with Terraform (serverless ACI)
* ✅ **CI pipeline** using GitHub Actions
* ✅ **Manual CD workflow** demonstrating professional deployment

---

## 📖 References

* [UCI Machine Learning Repository – Physiotherapy Dataset](https://archive.ics.uci.edu/ml/datasets/physiotherapy+exercises)
````
