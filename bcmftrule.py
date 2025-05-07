def check_bc_fuel_tax_applicability(
    fuel_type: str,
    origin: str,  # 'manufactured' or 'imported'
    is_collector: bool,
    is_first_sale: bool,
    purchaser_type: str,  # 'collector', 'registered_reseller', 'end_user', 'export'
    use_case: str,        # 'engine_use', 'non_engine_use', 'export', 'resale'
    certificate: str = None,
    destination: str = "british_columbia"
) -> tuple[bool, list[str]]:
    references = []

    # Check for missing required fields
    if not destination:
        return True, ["Missing required field: 'destination'. Cannot assess exemption. [MFT Act s.73]"]

    # General rule: MFT applies on fuel used in internal combustion engines in BC
    if use_case == "engine_use" and destination == "british_columbia":
        references.append("Fuel is used in an internal combustion engine in BC. [MFT Act s.73, Bulletin MFT-CT 001]")
        tax_applicable = True

        # Check for specific exemptions
        if fuel_type == "propane" and certificate in ["farm_use", "resale", "diplomat", "common_carrier"]:
            references.append(f"Exempt due to valid certificate for {certificate.replace('_', ' ')}. [MFT Reg s.85, Bulletin MFT-CT 005]")
            tax_applicable = False
        elif purchaser_type == "registered_reseller":
            references.append("Exempt: Sale to Registered Reseller with resale intent. [MFT Reg s.79, Bulletin MFT-CT 002]")
            tax_applicable = False
        elif purchaser_type == "collector":
            references.append("Exempt: Sale to another Collector. [MFT Act s.76]")
            tax_applicable = False

    # Export scenario — fuel leaving BC
    elif destination != "british_columbia":
        references.append(f"Fuel destined for export to {destination.title()}. [MFT Reg s.80, Bulletin MFT-CT 001]")
        if certificate in ["export", "resale"]:
            references.append("Exempt: Export or resale certificate provided. [MFT Reg s.81]")
            tax_applicable = False
        else:
            references.append("Tax not applicable due to out-of-province delivery. [MFT Act s.73]")
            tax_applicable = False

    # Resale scenario
    elif use_case == "resale" and purchaser_type in ["registered_reseller", "collector"]:
        references.append("Exempt: Fuel resold to a qualified reseller or collector. [MFT Reg s.79]")
        tax_applicable = False

    # Default: tax applies
    else:
        references.append("Default rule applied: MFT applies due to internal BC use and no qualifying exemption. [MFT Act s.73]")
        tax_applicable = True

    return tax_applicable, references
