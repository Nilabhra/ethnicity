# Ethnicity.io
Predicts religion, gender and ethnicity given a name string for Indian names.

### How it works
Using bayesian models trained using string sequences. Data for gender was obtained by scraping CBSE results, while data for ethnicity and religion was scraped from a matrimonial site called SimplyMarry.

Takes in a name string as input, and returns the predicted gender, ethnicity and religion with associated probabilities.

### TODO
- Get more training data (!)
- Use better models - consider using RNNs. They are better for sequence based data.
- Design a (rate-limited) API for Ethnicity.io
