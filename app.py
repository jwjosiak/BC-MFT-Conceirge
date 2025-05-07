# app.py

import streamlit as st
from bcmftrule import check_bc_fuel_tax_applicability  # Match filename exactly

st.set_page_config(page_title="BC Motor Fuel Tax Tool", layout="centered")
st.title("🚛 BC Motor Fuel Tax Determination Tool")

with st.expander("ℹ️ Help"):
    st.markdown("""
    This tool assumes **you are not charging BC Motor Fuel Tax**.

    It will check whether your exemption position is supported and list any missing documentation.

    ### ✅ How to use:
    - Fill in all known fields using the dropdowns
    - Choose “Not sure” if you lack specific information
    - Click outside the fields to refresh the result
    """)

st.subheader("📋 Enter Transaction Details")

# ---- INPUT FIELDS ----
fuel_type = st.selectbox("Fuel Type", ["Not sure", "Propane", "Gasoline", "Diesel", "Aviation Fuel", "Jet Fuel"])
origin = st.selectbox("Fuel Origin", ["Not sure", "Imported", "Manufactured in BC"])

is_collector = st.radio("Are you a registered Collector?", ["Not sure", "Yes", "No"])
is_collector = None if is_collector == "Not sure" else is_collector == "Yes"

is_first_sale = st.radio("Is this the first sale in BC after import/production?", ["Not sure", "Yes", "No"])
is_first_sale = None if is_first_sale == "Not sure" else is_first_sale == "Yes"

purchaser_type = st.selectbox("Purchaser Type", [
    "Not sure", "End User", "Registered Reseller", "Collector", "Retail Dealer", "Export"
])

use_case = st.selectbox("Use Case", [
    "Not sure", "Engine Use", "Resale", "Heating (Residential)", "Farm Use", "Export", "Non-Engine Use"
])

certificate = st.selectbox("Certificate Provided", [
    "None / Not sure", "Common Carrier", "Resale", "Farm Use", "Residential Heating", "Diplomat"
])

bc_zone = st.selectbox("BC Zone (if applicable)", ["Not sure", "Zone I", "Zone II", "Zone III"])
destination = st.selectbox("Final Destination of Fuel", ["Not sure", "BC", "Outside BC"])
title_transfer_location = st.selectbox("Where Did Title Transfer Occur?", ["Not sure", "BC", "Outside BC"])

# ---- PREP INPUTS FOR RULE ENGINE ----
inputs = {
    "fuel_type": fuel_type.lower() if fuel_type != "Not sure" else None,
    "origin": origin.lower() if origin != "Not sure" else None,
    "is_collector": is_collector,
    "is_first_sale": is_first_sale,
    "purchaser_type": purchaser_type.lower().replace(" ", "_") if purchaser_type != "Not sure" else None,
    "use_case": {
        "Engine Use": "engine_use",
        "Resale": "resale",
        "Heating (Residential)": "heating",
        "Farm Use": "farm_use",
        "Export": "export",
        "Non-Engine Use": "non_engine_use"
    }.get(use_case, None),
    "certificate": certificate.lower().replace(" ", "_") if certificate != "None / Not sure" else None,
    "bc_zone": bc_zone if bc_zone != "Not sure" else None,
    "destination": destination.upper() if destination != "Not sure" else None,
    "title_transfer_location": title_transfer_location.upper() if title_transfer_location != "Not sure" else None
}

# ---- DECISION LOGIC ----
if inputs["fuel_type"]:  # only check if fuel_type is specified
    st.subheader("⚖️ MFT Exemption Guidance")
    is_supported, message = check_bc_fuel_tax_applicability(**inputs)

    if is_supported:
        st.success("✅ You may proceed without charging MFT.")
        st.markdown(f"**Reason:** {message}")
    else:
        st.error("⚠️ Charging no MFT is not currently supported.")
        st.markdown(f"**Action Required:** {message}")

    with st.expander("🧪 View input data (for audit/debugging)"):
        st.json(inputs)
