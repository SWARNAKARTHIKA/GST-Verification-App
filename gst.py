import streamlit as st
import pandas as pd
import requests
import time

def fetch_gst_details(gst_number, api_url, api_headers=None):
    try:
        formatted_url = api_url.format(gst_number)
        response = requests.get(formatted_url, headers=api_headers)
        
        if response.status_code == 200 and response.json().get("flag"):
            data = response.json().get("data")
            return {
                "GSTIN/UIN": data.get("gstin", ""),
                "Name": data.get("tradeNam", ""),
                "Address": data.get("pradr", {}).get("adr", ""),
                "State": data.get("stj", "").split(",")[0].split(" - ")[1] if "State" in data.get("stj", "") else "",
                "Country": "India",
                "Registration Type": data.get("dty", "")
            }
        else:
            return {"Error": "Invalid GSTIN or API Response"}
    except Exception as e:
        return {"Error": str(e)}

def main():
    st.title("GST Details")
    st.write("Upload an Excel sheet with GST Numbers.")

    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        if "GSTIN/UIN" not in df.columns:
            st.error("The Excel file must contain a column named 'GSTIN/UIN'.")
            return

        st.write("Uploaded GST Numbers:")
        st.dataframe(df)

        API_URL = "http://sheet.gstincheck.co.in/check/3044986ae527ae006c870bdc066a1469/{}"
        API_HEADERS = {}

        results = []

        st.write("Fetching details, please wait...")
        progress_bar = st.progress(0)
        total_rows = len(df)

        for idx, gst_number in enumerate(df["GSTIN/UIN"]):
            gst_details = fetch_gst_details(gst_number, API_URL, API_HEADERS)
            if "Error" in gst_details:
                st.warning(f"Error fetching details for GSTIN: {gst_number}")
                continue

            results.append(gst_details)

            progress_bar.progress((idx + 1) / total_rows)
            time.sleep(0.5)

        if results:
            result_df = pd.DataFrame(results)

            st.write("Fetched GST Details:")
            st.dataframe(result_df)

            output_file = "gst_details_output.xlsx"
            result_df.to_excel(output_file, index=False)

            with open(output_file, "rb") as f:
                st.download_button(
                    label="Download Excel File with GST Details",
                    data=f,
                    file_name="gst_details_output.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.error("No GST details were fetched. Please check your API or input file.")

if __name__ == "__main__":
    main()
