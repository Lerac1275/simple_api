# Introduction

Welcome to the main project folder!

For a quick guide on how the dashboard works please refer to the main README page at the home directory for this project. 

# `dashboard.py`
This is the main dashboard run as a `streamlit` app. The API calls to `coinGecko` & certain data transformations are abstracted out into `geckoAdmin.py`, while the graphing components are abstracted out into `grapher.py`.

# `unit_test.py`
This is the python file used to run unit tests for this project. 

Since there is currently no `pytest` framework for `streamlit` applications as a whole, this project tests the individual components that feed into the main dashboard. 
