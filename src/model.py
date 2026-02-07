from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class Scenario:
    scenario_id: str
    name: str
    org_size: str
    industry: str
    user_count: int
    compliance_pressure: str
    regulatory_environment: List[str]
    it_environment: str
    cloud_email: str
    remote_access: str
    endpoint_management: str
    iam_maturity: str
    data_sensitivity: str
    data_protection_maturity: str
    backup_maturity: str
    logging_monitoring_maturity: str
    payment_processing: bool
    customer_data_volume: str
    third_party_vendors: str

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Scenario":
        return Scenario(
            scenario_id=str(d["scenario_id"]),
            name=str(d["name"]),
            org_size=str(d["org_size"]),
            industry=str(d["industry"]),
            user_count=int(d["user_count"]),
            compliance_pressure=str(d["compliance_pressure"]),
            regulatory_environment=list(d.get("regulatory_environment", [])),
            it_environment=str(d["it_environment"]),
            cloud_email=str(d["cloud_email"]),
            remote_access=str(d["remote_access"]),
            endpoint_management=str(d["endpoint_management"]),
            iam_maturity=str(d["iam_maturity"]),
            data_sensitivity=str(d["data_sensitivity"]),
            data_protection_maturity=str(d["data_protection_maturity"]),
            backup_maturity=str(d["backup_maturity"]),
            logging_monitoring_maturity=str(d["logging_monitoring_maturity"]),
            payment_processing=bool(d["payment_processing"]),
            customer_data_volume=str(d["customer_data_volume"]),
            third_party_vendors=str(d["third_party_vendors"]),
        )
