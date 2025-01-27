# GST Details Fetcher

A **Streamlit**-based web application for validating and retrieving GSTIN/UIN details from an uploaded Excel sheet. This app uses a public API to fetch GST information and provides the output as a downloadable Excel file.

---

## Features

- **Excel Upload**: Easily upload an Excel sheet containing GSTIN/UIN numbers.
- **GST Verification**: Validate and fetch details for each GSTIN/UIN using a public API.
- **Real-Time Status Updates**: Displays the progress of fetching GST details for all records.
- **Error Handling**: Identifies and warns users about invalid GSTINs or failed API responses.
- **Export Results**: Download the results in Excel format with enriched GST details.

---

## Installation

To run this application locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/your-repository-name.git
   cd your-repository-name
   pip install -r requirements.txt
   streamlit run app.py

