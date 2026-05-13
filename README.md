# Epoch — Market Regime Analysis Engine

A terminal-based machine learning system that classifies current 
market conditions into distinct volatility regimes using an original 
trained Gaussian Mixture Model on historical price data.

---

## Status
🚧 In Progress

---

## What It Does

Epoch analyzes historical market data and classifies what regime 
the market is currently in — Bull/Trending, Sideways/Neutral, 
High Volatility, or Crisis/Bear — without any labeled training data.

---

## Tech Stack

- Python
- scikit-learn — GMM implementation
- pandas / numpy — feature engineering
- yfinance — market data pipeline
- scipy — statistical validation
- matplotlib — validation chart generation
- rich — terminal interface
- joblib — model persistence

---

## Project Structure

```
epoch/
├── data/
│   └── fetcher.py          
├── features/
│   └── engineer.py         
├── models/
│   ├── regime.py           
│   └── saved/              
├── validation/
│   └── validator.py        
├── outputs/
│   └── charts/             
├── experiments/            
├── tests/                  
├── config.py               
├── main.py                 
└── requirements.txt
```

---

## Author

Chase Meyers | CS @ University of Tennessee, Knoxville
