# 🧠 Automated Fact-Checking Prediction Using Machine Learning

![Pinocchio](./politifact.png)




## 🔍 Project Overview

In an era of viral misinformation, this project aims to build an **automated fact-checking system** using machine learning. Leveraging labeled claims from [PolitiFact.com](https://www.politifact.com/), the model classifies public statements into six credibility levels:  
**True**, **Mostly True**, **Half True**, **Mostly False**, **False**, and **Pants on Fire**.

The final model was deployed using FastAPI and Google Cloud, offering a user-facing interface to assess the credibility of new claims.

🌐 **Live App**: [Try the Fact-Checker →](https://fastapi-app-273008876300.us-central1.run.app/)

---

## 📂 Table of Contents

- [📄 Source Data](#source-data)
- [📚 Notebooks](#notebooks)
- [📑 Documents](#documents)
- [⚙️ Model Overview](#model-overview)
- [🚀 Deployment](#deployment)
- [🛠️ Future Work](#future-work)

---

## 📄 Source Data

- **Original Labeled Statements**: Scraped from [PolitiFact.com](https://www.politifact.com/)
- **Metadata Includes**:
  - Statement text
  - Speaker/source
  - Statement date
  - Labeled credibility (by human fact-checkers)

---

## 📚 Notebooks

- `EDA.ipynb` — Data Wrangling & Visualization  
- `ML.ipynb` — Model Training and Evaluation  
- `Evaluation_Report-3.ipynb` — Final Model Interpretation  
- `Fine_Tuning.ipynb` — GridSearchCV and Hyperparameter Tuning  
- `Flask.ipynb` — First Deployment Steps  
- `Deep_Learning.ipynb` — Experimentation with DNN  
- `Trees_and_Forests.ipynb` — Tree-based Models  
- `Recommendation_Engines.ipynb` — Auxiliary ML Exploration

_Notebooks not used in final deployment are stored in the `extras/` folder._

---

## 📑 Documents

- 📘 [Final Report (PDF)](./Automated%20Fact-Checking%20Prediction%20Using%20Machine%20Learning.pdf)

  Detailed explanation of methodology, challenges, and findings.

- 🖥️ Slide Deck (coming soon)

---

## ⚙️ Model Overview

- Models Tested: Naive Bayes, Logistic Regression, SVM, XGBoost, Random Forest
- Best Model: **Logistic Regression** (Macro AUC = 0.7485)
- Key Features:
  - Cleaned and tokenized statements
  - One-hot encoded source categories
  - Temporal patterns from publication dates
- Interpretability:
  - Predictive word analysis using conditional probability with smoothing
  - Clear association between certain terms and credibility labels

---

## 🚀 Deployment

The final model is deployed on Google Cloud Run using FastAPI:

🌐 [Access the Deployed App](https://fastapi-app-273008876300.us-central1.run.app/)

---

## 🛠️ Future Work

- Automate real-time data scraping from PolitiFact
- Implement NER for better speaker/source classification
- Explore transformer-based architectures like BERT for deeper language understanding

---

## 📸 Acknowledgments

- Data Source: [PolitiFact.com](https://www.politifact.com/)


---

