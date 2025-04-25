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
- **Scraping Notebook**: [`scrapping_data.ipynb`](./scrapping_data.ipynb)
  - [`politifact.csv`](./politifact.csv) — Structured dataset of labeled statements scraped from PolitiFact.com.  
  This file contains metadata including the statement text, speaker, rating, and publication date, used to train and evaluate fact-checking models.  
  > *This dataset was collected for educational and research purposes only. All original content and rights remain with [PolitiFact.com](https://www.politifact.com).*
- **Metadata Includes**:
  - Statement text
  - Speaker/source
  - Statement date
  - Labeled credibility (by human fact-checkers)

---

##  Notebooks
- [`ML.ipynb`](./ML%20.ipynb) — Data Wrangling & Visualization
- [`Evaluation_Report-3.ipynb`](./Evaluation_Report-3.ipynb) — Final Model Interpretation
 
A variety of models were evaluated, including Naive Bayes, Logistic Regression, SVM, XGBoost, and Random Forest.  
**Logistic Regression** was selected for its balance of performance and efficiency.





---

## Documents

- [Final Report (PDF)](./Automated%20Fact-Checking%20Prediction%20Using%20Machine%20Learning.pdf)

  Detailed explanation of methodology, challenges, and findings.















---

