"""Command-Line Interface (CLI) for SatarkBharat Pre-Transaction Sentinel Engine."""

import argparse
import json
import sys

from satark_bharat.decision.threat_engine import ThreatIndexEngine
from satark_bharat.redressal.dossier import DossierGenerator
from satark_bharat.redressal.router import RegulatoryRouter


def main():
    parser = argparse.ArgumentParser(
        prog="satark",
        description="SatarkBharat — Multimodal Pre-Transaction Investor Defense Sentinel CLI",
    )
    parser.add_argument("text", nargs="?", help="Advisory chat message or claims text to audit")
    parser.add_argument("--json", action="store_true", help="Output full structured JSON dossier")
    parser.add_argument("--sms", action="store_true", help="Output 1930 Cyber Cell formatted SMS dispatch")

    args = parser.parse_args()

    if not args.text:
        # Check stdin
        if not sys.stdin.isatty():
            input_text = sys.stdin.read().strip()
        else:
            parser.print_help()
            sys.exit(1)
    else:
        input_text = args.text

    engine = ThreatIndexEngine()
    report = engine.evaluate(input_text)
    route = RegulatoryRouter.resolve_route(report)
    dossier = DossierGenerator.generate_json_dossier(report, input_text)

    if args.json:
        print(json.dumps(dossier, indent=2))
        return

    if args.sms:
        print(DossierGenerator.generate_1930_sms(report, dossier["incident_id"]))
        return

    # Beautiful minimal terminal readout
    status_icon = "🔴" if report.composite_threat_score >= 60 else "🟢"
    print("\n" + "=" * 60)
    print(f"🛡️  SATARK BHARAT SENTINEL REPORT  [{dossier['incident_id']}]")
    print("=" * 60)
    print(f"Threat Score:      {report.composite_threat_score}/100 ({report.severity}) {status_icon}")
    print(f"Designated Route:  {route.portal_name}")
    print(f"Statutory Basis:   {route.statutory_basis}")
    print("-" * 60)
    print(f"English Summary:   {report.plain_english_summary}")
    print(f"Hindi Advisory:    {report.vernacular_hindi_summary}")
    print(f"Bengali Advisory:  {report.vernacular_bengali_summary}")
    print("-" * 60)
    print("Regulatory Violations:")
    if report.statutory_violations:
        for v in report.statutory_violations:
            print(f" • {v}")
    else:
        print(" • None (Compliant with SEBI & NSDL Invariants)")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
