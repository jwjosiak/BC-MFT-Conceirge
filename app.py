import streamlit as st
from bcmftrule import check_bc_fuel_tax_applicability

# Streamlit page setup
st.set_page_config(
    page_title="BC Motor Fuel Tax Tool",
    page_icon="🚛",
    layout="centered"
)

# Header
st.title("🚛 BC Motor Fuel Tax Determination Tool")
st.markdown("Determine if Motor Fuel Tax applies using the **BC Motor Fuel Tax Act**, **Regulations**, and relevant **Bulletins**.")
st.markdown("---")

# Input form layout
st.markdown("### 🔍 Enter Transaction Details")

col1, col2 = st.columns(2)

with col1:
    fuel_type = st.selectbox("Fuel Type", ["Propane", "Gasoline", "Diesel", "Aviation Fuel", "Marine Fuel"])
    origin = st.selectbox("Origin", ["Manufactured in BC", "Imported into BC"])
    is_collector = st.radio("Are you a Collector?", ["Yes", "No"]) == "Yes"

with col2:
    is_first_sale = st.radio("Is this the first sale after manufacture or import?", ["Yes", "No"]) == "Yes"
    purchaser_type = st.selectbox("Purchaser Type", ["Collector", "Registered Reseller", "End User", "Export"])
    use_case = st.selectbox("Use of Fuel", ["Engine Use", "Non-Engine Use", "Export", "Resale"])

certificate = st.selectbox("Certificate Provided (if applicable)", [None, "Resale", "Farm Use", "Diplomat", "Common Carrier"])
destination = st.selectbox("Fuel Destination", [
    "British Columbia", 
    "Alberta", 
    "Saskatchewan", 
    "Manitoba", 
    "USA", 
    "International"
])

# Run the rule engine
if st.button("Run MFT Determination"):
    tax_applicable, references = check_bc_fuel_tax_applicability(
        fuel_type=fuel_type.lower(),
        origin="manufactured" if origin == "Manufactured in BC" else "imported",
        is_collector=is_collector,
        is_first_sale=is_first_sale,
        purchaser_type=purchaser_type.lower().replace(" ", "_"),
        use_case=use_case.lower().replace(" ", "_"),
        certificate=certificate.lower().replace(" ", "_") if certificate else None,
        destination=destination.lower().replace(" ", "_")
    )

    # Output results
    st.markdown("### 📋 Determination")
    if tax_applicable:
        st.error("Motor Fuel Tax **applies** to this transaction.")
    else:
        st.success("Motor Fuel Tax **does NOT apply** to this transaction.")

    # Show references from Act, Regs, Bulletins
    st.markdown("### 📚 References")
    for ref in references:
        st.markdown(f"- {ref}")

st.markdown("---")
st.caption("Built with ❤️ by the Tax Team")
