# Market Risk & VaR Analyzer

A small Python script that calculates basic risk metrics for a 4-stock
portfolio (AAPL, MSFT, GOOGL, AMZN, equal-weighted) using free historical
price data.

Built with `yfinance`, `pandas`, `numpy`, and `scipy`.

---

## Setup

```powershell
cd market-risk-var-analyzer

python -m venv venv
venv\Scripts\Activate.ps1

pip install yfinance pandas numpy scipy
```

## Run

```powershell
python risk_analyzer.py
```

Output prints to the terminal.

<img width="429" height="398" alt="output" src="https://github.com/user-attachments/assets/6a50d2cd-662d-42d0-ae82-a1fd41a379b0" />



## What it calculates

| Step | What it does |
|---|---|
| Download prices | Pulls daily closing prices since 2021 via `yfinance` |
| Daily returns | Converts prices to daily % change |
| Annualized volatility | Scales daily std dev by √252 |
| Correlation matrix | Shows how much the 4 stocks move together |
| Portfolio returns | Combines the 4 stocks' returns into one weighted daily series |
| Historical VaR (95%) | 5th percentile of actual historical daily returns |
| Parametric VaR (95%) | Same idea, assuming a normal distribution (mean + z-score × std) |
| Risk contribution | Uses the covariance matrix to show which asset contributes most to portfolio risk |

---

## Sample output (one actual run)

```
Portfolio 1-day Historical VaR (95%): 2.60% -> $25,998
Portfolio 1-day Parametric VaR (95%): 2.49% -> $24,933

--- Risk Contribution by Asset ---
AAPL     21.4%
AMZN     30.1%
GOOGL    26.1%
MSFT     22.4%
```

These numbers are specific to the date range and 4 tickers hardcoded in the
script, and will change slightly each time it's rerun since the data window
keeps moving forward. On this run: Historical and Parametric VaR came out
close to each other, and AMZN's share of portfolio risk (30.1%) was higher
than its 25% position weight.

---

## Limitations

- Only 4 tickers, equal weights, one fixed date range — not tested against
  other portfolios or time periods.
- Parametric VaR assumes normally distributed returns, which is a known
  simplification — real stock returns often have fatter tails than a normal
  distribution predicts.
- `yfinance` occasionally returns an empty response on a given run (a
  Yahoo-side issue, not a bug in the script) — rerunning usually fixes it.
- No backtesting was done to check how often actual losses exceeded the VaR
  estimate.

---

## What this project covers

- Historical VaR and Parametric VaR, and how they differ
- Correlation and covariance matrices
- Marginal risk contribution by asset
