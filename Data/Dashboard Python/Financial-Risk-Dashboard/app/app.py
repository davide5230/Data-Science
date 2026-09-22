#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# imports necessary libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from utils import compute_technical_indicators, prepare_lag_features

# app.py
app = dash.Dash(__name__)
app.title = 'Financial Risk Dashboard'

default_ticker = 'AAPL'

app.layout

