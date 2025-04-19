# Automated Fact-Checking Prediction Using Machine Learning

![Pinocchio](./politifact.png)




##  Project Overview

In an era of viral misinformation, this project aims to build an **automated fact-checking system** using machine learning. Leveraging labeled claims from [PolitiFact.com](https://www.politifact.com/), the model classifies public statements into six credibility levels:  
**True**, **Mostly True**, **Half True**, **Mostly False**, **False**, and **Pants on Fire**.

The final model was deployed using FastAPI and Google Cloud, offering a user-facing interface to assess the credibility of new claims.

 **Live App**: [Try the Fact-Checker →](https://fastapi-app-273008876300.us-central1.run.app/)

---




##  Source Data

- **Original Labeled Statements**: Scraped from [PolitiFact.com](https://www.politifact.com/)
- **Scraping Notebook**: [`Copy_of_BeautifulSoupPractice.ipynb`](./Copy_of_BeautifulSoupPractice.ipynb)
  - [`politifact.csv`](./politifact.csv) — Structured dataset of labeled statements scraped from PolitiFact.com.  
  This file contains metadata including the statement text, speaker, rating, and publication date, used to train and evaluate fact-checking models.  
  > ⚠️ *For educational and research purposes only. All content originally sourced from [PolitiFact.com](https://www.politifact.com/). Rights remain with the original publisher.*

- **Metadata Includes**:
  - Statement text
  - Speaker/source
  - Statement date
  - Labeled credibility (by human fact-checkers)

---

##  Notebooks
- [`ML (2).ipynb`](./ML%20(2).ipynb) — Data Wrangling & Visualization
- [`Evaluation_Report-3.ipynb`](./Evaluation_Report-3.ipynb) — Final Model Interpretation




_Notebooks not used in final deployment are stored in the `extras/` folder._

---

## Documents

- [Final Report (PDF)](./Automated%20Fact-Checking%20Prediction%20Using%20Machine%20Learning.pdf)

  Detailed explanation of methodology, challenges, and findings.



---

##  Model Overview

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



## 📸 Acknowledgments

- Data Source: [PolitiFact.com](https://www.politifact.com/)


---

