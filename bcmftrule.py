# bcmftrule.py

def check_bc_fuel_tax_applicability(
    fuel_type: str,
    origin: str,
    is_collector: bool,
    is_first_sale: bool,
    purchaser_type: str,
    use_case: str,
    certificate: str = None,
    bc_zone: str = None,
    destination: str = None,
    title_transfer_location: str = None
):
    """
    Assumes seller will not charge MFT. Returns:
    (is_supported: bool, message: str with reasoning + references)
    """

    # Normalize inputs
    fuel_type = fuel_type.lower() if fuel_type else None
    purchaser_type = purchaser_type.lower() if purchaser_type else None
    use_case = use_case.lower() if use_case else None
    certificate = certificate.lower() if certificate else None
    bc_zone = bc_zone.title() if bc_zone else None
    destination = destination.upper() if destination else None
    title_transfer_location = title_transfer_location.upper() if title_transfer_location else None

    required_fields = ["fuel_type", "use_case", "purchaser_type", "destination", "title_transfer_location"]
    for field in required_fields:
        if not locals()[field]:
            return False, f"Missing required field: '{field}'. Cannot assess exemption. [MFT Act s. 73]"

    # EXPORT
    if use_case == "export" or destination != "BC":
        if certificate == "common_carrier":
            return True, (
                "✅ Export exemption applies. Common Carrier Certificate on file. "
                "[Ref: MFT Act s. 1, s. 74(1)(e); Bulletin MFT-CT 005]"
            )
        return False, (
            "❌ To exempt exports, obtain a Common Carrier Certificate. "
            "[Ref: MFT Act s. 1 'export', s. 74(1)(e); Bulletin MFT-CT 005]"
        )

    # RESALE
    if use_case == "resale":
        if purchaser_type in ["collector", "registered_reseller"] and certificate == "resale":
            return True, (
                "✅ Resale exemption valid with resale certificate and registered purchaser. "
                "[Ref: MFT Reg s. 39; Bulletin MFT-CT 003]"
            )
        return False, (
            "❌ Resale exemption denied. Ensure purchaser is registered and resale certificate is on file. "
            "[Ref: MFT Reg s. 39; Bulletin MFT-CT 003]"
        )

    # HEATING (Propane)
    if fuel_type == "propane" and use_case == "heating":
        if certificate == "residential_heating" and bc_zone in ["Zone II", "Zone III"]:
            return True, (
                "✅ Residential heating exemption applies with zone and certificate. "
                "[Ref: Bulletin MFT-CT 004; MFT Reg Zones]"
            )
        return False, (
            "❌ Propane heating exemption denied. Must provide Residential Heating Certificate and be in Zone II or III. "
            "[Ref: Bulletin MFT-CT 004]"
        )

    # FARM USE
    if use_case == "farm_use":
        if certificate == "farm_use":
            return True, (
                "✅ Farm use exemption supported by Farm Fuel Certificate. "
                "[Ref: MFT Reg s. 18; Bulletin MFT-CT 006]"
            )
        return False, (
            "❌ Farm use exemption denied. Certificate required. "
            "[Ref: MFT Reg s. 18; Bulletin MFT-CT 006]"
        )

    # DIPLOMATIC
    if certificate == "diplomat":
        return True, (
            "✅ Diplomatic exemption allowed. "
            "[Ref: CRA & BC Finance diplomatic tax relief policies]"
        )

    # ENGINE USE
    if use_case == "engine_use":
        if fuel_type == "propane" and certificate in ["farm_use", "residential_heating"] and bc_zone in ["Zone II", "Zone III"]:
            return True, (
                "✅ Propane exemption for engine use in special case with cert and zone. "
                "[Ref: Bulletins MFT-CT 004 & 006]"
            )
        return False, (
            "❌ Engine use is taxable unless a very specific propane exemption applies. "
            "[Ref: MFT Act s. 73(1)]"
        )

    # NON-ENGINE USE
    if use_case == "non_engine_use":
        return False, (
            "❌ MFT generally applies. Documented industrial use (e.g. feedstock, steam) required for case-by-case exemption. "
            "[Ref: MFT Act s. 73; CRA indirect use guidance]"
        )

    # DEFAULT
    return False, (
        "❌ No exemption conditions met. MFT must be charged unless supported by specific documentation. "
        "[Ref: MFT Act s. 73; Bulletins MFT-CT 003–006]"
    )
