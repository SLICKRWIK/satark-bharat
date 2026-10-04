"""Payment Channel & UPI Virtual Payment Address (VPA) Clearing Auditor."""

from dataclasses import dataclass

from satark_bharat.config import UPI_VPA_REGEX


@dataclass
class PaymentAuditResult:
    detected_vpas: list[str]
    primary_vpa: str | None
    is_personal_vpa: bool
    is_clearing_compliant: bool
    provider_bank: str | None
    statutory_violation: str | None
    penalty_points: int


class PaymentChannelAuditor:
    # Common personal consumer PSP handles on UPI
    PERSONAL_PSP_HANDLES = {
        "okhdfcbank", "okaxis", "oksbi", "okicici", "ybl", "ibl", "paytm", "apl",
        "postbank", "ptaxis", "ptyes", "axl", "upi"
    }

    # Known authorized corporate/merchant aggregator prefixes or suffixes
    MERCHANT_INDICATORS = {
        "razorpay", "billdesk", "ccavenue", "payu", "cashfree", "nse", "bse", "zerodha", "groww"
    }

    def extract_vpas(self, text: str) -> list[str]:
        matches = UPI_VPA_REGEX.findall(text)
        return list(dict.fromkeys(matches))

    def audit_payment(self, text: str) -> PaymentAuditResult:
        vpas = self.extract_vpas(text)

        if not vpas:
            return PaymentAuditResult(
                detected_vpas=[],
                primary_vpa=None,
                is_personal_vpa=False,
                is_clearing_compliant=True,
                provider_bank=None,
                statutory_violation=None,
                penalty_points=0,
            )

        primary = vpas[0]
        handle, _, provider = primary.partition("@")
        provider_lower = provider.lower()

        is_personal = False
        if provider_lower in self.PERSONAL_PSP_HANDLES:
            is_personal = True

        # Check if handle has numbers or personal name patterns
        if any(c.isdigit() for c in handle) and is_personal:
            is_personal = True

        # Check if explicitly corporate merchant
        if any(corp in handle.lower() or corp in provider_lower for corp in self.MERCHANT_INDICATORS):
            is_personal = False

        if is_personal:
            violation = "Violation of SEBI Circular SEBI/HO/MIRSD/MIRSD-PoD-1/P/CIR/2023/71 (Advisory fees/trading deposits solicited to private personal UPI account rather than designated Clearing/Escrow account)"
            penalty = 25
        else:
            violation = None
            penalty = 0

        return PaymentAuditResult(
            detected_vpas=vpas,
            primary_vpa=primary,
            is_personal_vpa=is_personal,
            is_clearing_compliant=not is_personal,
            provider_bank=provider,
            statutory_violation=violation,
            penalty_points=penalty,
        )
