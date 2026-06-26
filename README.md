# Explainable Stock Price Movement Prediction

Master's Project | Universiti Tunku Abdul Rahman (UTAR)

## Project Description

This project aims to predict the next-day price movement of banking stocks listed on Bursa Malaysia and the Singapore Exchange (SGX). The main objective is not only to make predictions but also to understand the factors that influence those predictions through explainable artificial intelligence (XAI).

The project uses the XGBoost machine learning algorithm together with SHAP (SHapley Additive exPlanations) to provide insights into how different features contribute to each prediction.

## Stocks Included

### Malaysia

* Maybank
* Public Bank
* CIMB
* RHB Bank
* Hong Leong Bank
* AmBank
* Alliance Bank
* AFFIN Bank
* Bank Islam Malaysia Berhad (BIMB)

### Singapore

* DBS
* OCBC
* UOB

## Technologies Used

* Python
* yfinance
* pandas-ta
* XGBoost
* SHAP
* Streamlit
* Git and GitHub

## Project Features

* Collects historical stock market data
* Generates technical indicators for feature engineering
* Predicts next-day stock price direction (Up or Down)
* Provides SHAP explanations for model predictions
* Interactive dashboard built with Streamlit

## Repository Setup

Clone the repository:

```bash
git clone https://github.com/yourusername/stock-prediction-xai-shap.git
cd stock-prediction-xai-shap
```
