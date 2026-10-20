"""PWR-001: mains exposure risk assessment, never a mains enable command.

230 V equipment is hazardous. This module deliberately cannot energize any
physical circuit, and reviewed configurations still need independent tests.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class MainsSafetyEvidence:
    powered_from_mains: bool
    qualified_electrical_review: bool = False
    live_parts_inaccessible: bool = False
    insulating_barriers_verified: bool = False
    protective_earth_verified: bool = False
    leakage_protection_verified: bool = False
    strain_relief_verified: bool = False
    enclosure_ingress_verified: bool = False
    cable_and_reel_thermal_verified: bool = False
    protected_shutdown_verified: bool = False
    wet_area_separation_verified: bool = False
    inspection_fresh: bool = False

@dataclass(frozen=True)
class MainsSafetyDecision:
    robot_motion_authorized: bool
    mains_energization_authorized: bool
    review_state: str
    missing_controls: tuple[str, ...]

def assess_mains_safety(evidence: MainsSafetyEvidence) -> MainsSafetyDecision:
    """No state of this gate alone grants mains energization."""
    if not isinstance(evidence, MainsSafetyEvidence):
        return MainsSafetyDecision(False,False,"invalid_input",("safety_evidence",))
    if not evidence.powered_from_mains:
        return MainsSafetyDecision(
            False,False,"low_voltage_design_review_required",
            ("low_voltage_supply_and_drive_interlock_verification",))
    checks = (
        "qualified_electrical_review", "live_parts_inaccessible",
        "insulating_barriers_verified", "protective_earth_verified",
        "leakage_protection_verified", "strain_relief_verified",
        "enclosure_ingress_verified", "cable_and_reel_thermal_verified",
        "protected_shutdown_verified", "wet_area_separation_verified",
        "inspection_fresh")
    missing = tuple(name for name in checks if getattr(evidence,name) is not True)
    if missing:
        return MainsSafetyDecision(False,False,"mains_configuration_rejected",missing)
    return MainsSafetyDecision(
        False,False,"documentary_prechecks_complete_independent_certification_pending",())
