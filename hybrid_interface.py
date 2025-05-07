# hybrid_interface.py

from bcmftrul import check_bc_fuel_tax_applicability

def run_hybrid_interface():
    print("🌲 BC Motor Fuel Tax CLI Tool")
    print("Assumes you will NOT charge MFT — this tool tells you what’s required to support that.")
    print("Type 'exit' at any time to quit.\n")

    while True:
        fuel_type = input("Fuel Type (propane, gasoline, diesel, etc.): ").strip().lower()
        if fuel_type == "exit": break

        origin = input("Origin (imported or manufactured): ").strip().lower()
        is_collector = input("Are you a collector? (yes/no): ").strip().lower()
        is_first_sale = input("Is this the first sale in BC? (yes/no): ").strip().lower()
        purchaser_type = input("Purchaser Type (end_user, registered_reseller, collector, export): ").strip().lower()
        use_case = input("Use Case (engine_use, resale, heating, farm_use, export, non_engine_use): ").strip().lower()
        certificate = input("Certificate (common_carrier, resale, farm_use, residential_heating, diplomat, or blank): ").strip().lower()
        bc_zone = input("BC Zone (Zone I, Zone II, Zone III): ").strip().title()
        destination = input("Destination (BC or OUTSIDE BC): ").strip().upper()
        title_transfer_location = input("Title Transfer Location (BC or OUTSIDE BC): ").strip().upper()

        result, explanation = check_bc_fuel_tax_applicability(
            fuel_type=fuel_type,
            origin=origin,
            is_collector=True if is_collector == "yes" else False,
            is_first_sale=True if is_first_sale == "yes" else False,
            purchaser_type=purchaser_type,
            use_case=use_case,
            certificate=certificate if certificate else None,
            bc_zone=bc_zone if bc_zone else None,
            destination=destination,
            title_transfer_location=title_transfer_location
        )

        print("\n--- Result ---")
        print("✅ Exempt - You may proceed without charging MFT." if result else "❌ Not Exempt - MFT should be charged.")
        print("Explanation:", explanation)
        print("\n----------------------------\n")

if __name__ == "__main__":
    run_hybrid_interface()
