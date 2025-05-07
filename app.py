import streamlit as st

# Page config
st.set_page_config(page_title="BC Motor Fuel Tax Tool", page_icon="🛢️")

# Logo and Title
st.markdown("""
<div style='text-align: left; display: flex; align-items: center; gap: 10px;'>
    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAAyCAYAAAC9nV3UAAAACXBIWXMAAA7EAAAOxAGVKw4bAAABMElEQVRoge2XsU3DMBCFZ4qYi9rIltzCIszENnBE2YjWfEJDqUp0BdFymFPbCieiwjPbRZTbnkzRkU8mh4/3ON3eANvpKJfwWcVtHbFawU8ULaKjvBtRO+ls59jzebgFsGuULkL5PKzFkfC+xFfKn8CbBcmuUr/RaEvkyZIZQbiD8N8K2kYxcRFa28twtdVndKMYOYIqMtzKzBQFLKtFJ7X1SpFT2xVUG4MzTVKqMqa8D3Hp3aA+VvD8a/QRkThRnlH4MXKiFUrnBaCF0Ft+Sv3vVWENvWLl0+eIfE8K5WexuJG2tZ9XLvgOgSY4XThfUJjjXop0r7ZHr4k9o98qpSWONOgAAAABJRU5ErkJggg==" width="20" alt="BC Icon">
    <h3 style='margin: 0;'>BC Motor Fuel Tax Determination Tool</h3>
</div>
""", unsafe_allow_html=True)

st.write("---")

# Inputs
fuel_type = st.selectbox("Fuel Type", ["Gasoline", "Diesel", "Propane", "Natural Gas", "Aviation Fuel", "Other"])
origin = st.radio("Fuel Origin", ["Manufactured in BC", "Imported into BC"])
is_collector = st.checkbox("Are you a Collector?")
is_first_sale = st.checkbox("Is this the first sale after manufacture/import?")
purchaser_type = st.selectbox("Purchaser Type", ["Collector", "Registered Reseller", "End User", "Export"])
use_case = st.selectbox("Use Case", ["Engine Use", "Non-Engine Use", "Export", "Resale"])
zone = st.selectbox("BC Destination Zone", ["Zone 1", "Zone 2", "Zone 3", "Outside BC"])
certificate = st.text_input("Certificate (e.g. resale, farm_use, diplomat)")

# Decision logic placeholder
def check_bc_fuel_tax_applicability(fuel_type, origin, is_collector, is_first_sale, purchaser_type, use_case, zone, certificate):
    reasons = []
    tax_applicable = True

    if use_case.lower() == "engine use":
        reasons.append("Fuel is used in an internal combustion engine.")

        if fuel_type.lower() == "propane" and certificate in ["farm_use", "residential_heating"]:
            tax_applicable = False
            reasons.append("Exempt due to use of propane for farm or residential heating with proper certificate.")
        elif purchaser_type.lower() == "export":
            tax_applicable = False
            reasons.append("Exempt because the purchaser is exporting the fuel.")
    elif use_case.lower() == "non-engine use":
        tax_applicable = False
        reasons.append("Fuel not used in an internal combustion engine.")
    elif use_case.lower() == "export":
        tax_applicable = False
        reasons.append("Exported fuel is exempt from MFT.")
    elif use_case.lower() == "resale" and certificate == "resale":
        tax_applicable = False
        reasons.append("Fuel sold for resale with proper resale certificate.")

    if zone == "Outside BC":
        tax_applicable = False
        reasons.append("Destination is outside of BC, MFT does not apply.")

    return tax_applicable, reasons

# Submit button
if st.button("Check Tax Applicability"):
    tax, explanation = check_bc_fuel_tax_applicability(
        fuel_type, origin, is_collector, is_first_sale, purchaser_type, use_case, zone, certificate
    )

    if tax:
        st.error("Motor Fuel Tax is applicable.")
    else:
        st.success("Motor Fuel Tax is NOT applicable.")

    st.markdown("#### Reasoning:")
    for reason in explanation:
        st.markdown(f"- {reason}")

