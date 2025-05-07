import streamlit as st
from bcmftrule import check_bc_fuel_tax_applicability

# Set page config
st.set_page_config(
    page_title="BC Motor Fuel Tax Tool",
    page_icon="🚛",
    layout="centered"
)

# Title and intro
st.title("🚛 BC Motor Fuel Tax Determination Tool")
st.subheader("Quickly determine if Motor Fuel Tax (MFT) applies to your transaction.")

st.markdown("---")

# Input form
st.markdown("### 🔧 Provide Transaction Details")

col1, col2 = st.columns(2)

with col1:
    fuel_type = st.selectbox("Fuel Type", ["Propane", "Gasoline", "Diesel", "Aviation Fuel", "Marine Fuel"])
    origin = st.selectbox("Fuel Origin", ["Manufactured in BC", "Imported into BC"])
    is_collector = st.radio("Are you a Collector?", ["Yes", "No"]) == "Yes"

with col2:
    is_first_sale = st.radio("Is this the first sale after manufacture/import?", ["Yes", "No"]) == "Yes"
    purchaser_type = st.selectbox("Purchaser Type", ["Collector", "Registered Reseller", "End User", "Export"])
    use_case = st.selectbox("Use of Fuel", ["Engine Use", "Non-Engine Use", "Export", "Resale"])

certificate = st.selectbox("Certificate Type (if any)", [None, "Resale", "Farm Use", "Diplomat", "Common Carrier"])

# Button to evaluate
if st.button("🔍 Check MFT Applicability"):
    tax_applicable, reasons = check_bc_fuel_tax_applicability(
        fuel_type=fuel_type.lower(),
        origin="manufactured" if origin == "Manufactured in BC" else "imported",
        is_collector=is_collector,
        is_first_sale=is_first_sale,
        purchaser_type=purchaser_type.lower().replace(" ", "_"),
        use_case=use_case.lower().replace(" ", "_"),
        certificate=certificate.lower().replace(" ", "_") if certificate else None
    )

    st.markdown("### ✅ Result")
    if tax_applicable:
        st.error("MFT **applies** to this transaction.")
    else:
        st.success("MFT **does NOT apply** to this transaction.")

    with st.expander("📄 Explanation"):
        for reason in reasons:
            st.markdown(f"- {reason}")

st.markdown("---")
st.caption("Built with ❤️ for BC tax analysts.")
