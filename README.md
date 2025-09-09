
# 🚚 Food Delivery Dashboard 

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Interactive-orange?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Container-blue?logo=docker&logoColor=white)](https://www.docker.com/)


---

## 📌 Summary
An **interactive dashboard** for analyzing food delivery data, built with **Python and Streamlit**.  
The dashboard supports **two languages (English & Persian)** and allows users to explore delivery data in a clear and interactive way.

---

## داشبورد تحویل غذا
یک **داشبورد تعاملی** برای تحلیل داده‌های تحویل غذا که با **Python و Streamlit** ساخته شده است.  
این داشبورد از **دو زبان (انگلیسی و فارسی)** پشتیبانی می‌کند و امکان بررسی داده‌ها به شکل تعاملی فراهم می کند.

---

## 🚀 Online Demos
- **Streamlit Cloud:** [🔗 Live Demo]([...your-streamlit-link...](https://fooddeliverydashboard-h3mgtzznzknyv77jablvpj.streamlit.app/))  
- **Hugging Face (Dockerized):** [🐳 Live Demo]([...your-hugging-face-link...](https://huggingface.co/spaces/amin704/food-delivery-dashboard))

---

## 🗂️ Project Structure
```

food-delivery-dashboard/
│
├─ dataset_cleaning.py         # Cleans invalid coordinates
├─ main.py                     # Main dashboard application
├─ requirements.txt
├─ Food Delivery Dataset.csv
├─ Cleaned_Food_Delivery_Dataset.csv
├─ Dockerfile
└─ README.md

````

- `dataset_cleaning.py` : Cleans the dataset by removing rows with invalid or missing coordinates.  
- `main.py` : Main dashboard application.

---

## 🛠️ Built With
- **Python 3.11**
- **Libraries:** `streamlit`, `pandas`, `matplotlib`, `seaborn`, `pydeck`
- **Docker:** Ensures consistent execution across different systems

---

## ⚙️ Local Setup

This project is ready to run "out of the box" using Docker.

### 1️⃣ Clone the repository
```bash

git clone https://github.com/amin704/food-delivery-dashboard.git
cd food-delivery-dashboard

````

### 2️⃣ Build the Docker image

```bash
docker build -t food-delivery-dashboard .
```

### 3️⃣ Run the container

```bash
docker run -p 8501:8501 food-delivery-dashboard
```

### 4️⃣ Open the dashboard

Open your browser and navigate to `http://localhost:8501`.



---

## 📊 Dataset

The dashboard uses the [Food Delivery Dataset](https://www.kaggle.com/datasets/gauravmalik26/food-delivery-dataset?resource=download&select=train.csv), containing information such as driver age, ratings, weather conditions, and delivery time.

---

## 📝 Notes

1. The cleaned dataset (`Cleaned_Food_Delivery_Dataset.csv`) is **already included** in this repository. Running the cleaning script is optional and provided for demonstration purposes.
2. Docker ensures consistent execution across all systems.
3. The dashboard is **dual-language (English & Persian)** and can be extended for language switching.

