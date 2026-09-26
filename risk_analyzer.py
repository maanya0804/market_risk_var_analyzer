
import pandas as pd
import numpy as np
import yfinance as yf
from scipy.stats import norm


TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN"]
WEIGHTS = np.array([0.25, 0.25, 0.25, 0.25])
PORTFOLIO_VALUE = 1_000_000
CONFIDENCE = 0.95

prices = yf.download(TICKERS, start="2021-01-01", auto_adjust=True)["Close"]
print("PRICES SHAPE:", prices.shape)
print(prices.head())

returns = prices.pct_change().dropna()
print("RETURNS SHAPE:", returns.shape)

annual_vol = returns.std() * np.sqrt(252)
corr_matrix = returns.corr()

port_returns = returns.dot(WEIGHTS)

hist_var_pct = -np.percentile(port_returns, (1 - CONFIDENCE) * 100)
hist_var_usd = hist_var_pct * PORTFOLIO_VALUE

mu, sigma = port_returns.mean(), port_returns.std()
z = norm.ppf(1 - CONFIDENCE)                      # -1.645 for 95%
param_var_pct = -(mu + z * sigma)
param_var_usd = param_var_pct * PORTFOLIO_VALUE


cov_matrix = returns.cov() * 252
port_vol = np.sqrt(WEIGHTS @ cov_matrix @ WEIGHTS)
marginal_contrib = cov_matrix @ WEIGHTS / port_vol
risk_contrib_pct = (WEIGHTS * marginal_contrib) / port_vol
risk_contrib_pct = risk_contrib_pct / risk_contrib_pct.sum()

print("\n--- Annualized Volatility per Asset ---")
print(annual_vol.round(3))
 
print("\n--- Correlation Matrix ---")
print(corr_matrix.round(2))
 
print(f"\nPortfolio 1-day Historical VaR (95%): {hist_var_pct*100:.2f}% "
      f"-> ${hist_var_usd:,.0f}")
print(f"Portfolio 1-day Parametric VaR (95%): {param_var_pct*100:.2f}% "
      f"-> ${param_var_usd:,.0f}")
 
print("\n--- Risk Contribution by Asset ---")
print((risk_contrib_pct * 100).round(1).astype(str) + "%")
# %%
