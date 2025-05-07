# test_hybrid.py

import unittest
from bcmftrul import check_bc_fuel_tax_applicability

class TestBCMFTLogic(unittest.TestCase):

    def check_case(self, description, inputs, expected_result, must_contain):
        result, explanation = check_bc_fuel_tax_applicability(**inputs)
        self.assertEqual(result, expected_result, f"{description} - Unexpected result")
        self.assertIn(must_contain.lower(), explanation.lower(), f"{description} - Explanation mismatch")

    def test_export_with_common_carrier(self):
        self.check_case(
            "Export with common carrier cert",
            {
                "fuel_type": "propane",
                "origin": "imported",
                "is_collector": False,
                "is_first_sale": True,
                "purchaser_type": "export",
                "use_case": "export",
                "certificate": "common_carrier",
                "bc_zone": "Zone II",
                "destination": "OUTSIDE BC",
                "title_transfer_location": "OUTSIDE BC"
            },
            True,
            "export exemption applies"
        )

    def test_resale_missing_certificate(self):
        self.check_case(
            "Resale without certificate",
            {
                "fuel_type": "diesel",
                "origin": "manufactured",
                "is_collector": False,
                "is_first_sale": True,
                "purchaser_type": "registered_reseller",
                "use_case": "resale",
                "certificate": None,
                "bc_zone": "Zone I",
                "destination": "BC",
                "title_transfer_location": "BC"
            },
            False,
            "resale exemption denied"
        )

    def test_heating_in_zone_iii_with_certificate(self):
        self.check_case(
            "Heating in Zone III with cert",
            {
                "fuel_type": "propane",
                "origin": "imported",
                "is_collector": False,
                "is_first_sale": True,
                "purchaser_type": "end_user",
                "use_case": "heating",
                "certificate": "residential_heating",
                "bc_zone": "Zone III",
                "destination": "BC",
                "title_transfer_location": "BC"
            },
            True,
            "residential heating exemption"
        )

    def test_engine_use_regular(self):
        self.check_case(
            "Engine use (no exemption)",
            {
                "fuel_type": "diesel",
                "origin": "manufactured",
                "is_collector": False,
                "is_first_sale": True,
                "purchaser_type": "end_user",
                "use_case": "engine_use",
                "certificate": None,
                "bc_zone": "Zone I",
                "destination": "BC",
                "title_transfer_location": "BC"
            },
            False,
            "engine use is taxable"
        )

    def test_missing_required_field(self):
        result, explanation = check_bc_fuel_tax_applicability(
            fuel_type="diesel",
            origin=None,
            is_collector=False,
            is_first_sale=True,
            purchaser_type=None,
            use_case=None,
            certificate=None,
            bc_zone=None,
            destination=None,
            title_transfer_location=None
        )
        self.assertFalse(result)
        self.assertIn("missing required field", explanation.lower())

if __name__ == "__main__":
    unittest.main()
