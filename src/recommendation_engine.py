def generate_recommendation(package_name, metadata, typosquat_result, vuln_result, risk_result):
    """
    Risk analizi sonuçlarına göre somut bir aksiyon önerisi üretir.
    """
    category = risk_result["category"]

    # En kritik durum: paket bulunamadı (typo veya kaldırılmış/zararlı olabilir)
    if not metadata.get("found", True):
        if typosquat_result.get("is_suspicious"):
            suggested = typosquat_result["closest_match"]
            return {
                "action": "REPLACE_IMMEDIATELY",
                "message": (
                    f"'{package_name}' was not found on PyPI and closely resembles "
                    f"'{suggested}'. This strongly suggests a typo or typosquatting attempt. "
                    f"Replace with: {suggested}"
                ),
            }
        return {
            "action": "INVESTIGATE",
            "message": f"'{package_name}' was not found on PyPI. Verify the package name is correct.",
        }

    # Typosquat şüphesi var ama paket gerçekten var (nadir ama olabilir)
    if typosquat_result.get("is_suspicious"):
        suggested = typosquat_result["closest_match"]
        return {
            "action": "REVIEW",
            "message": (
                f"'{package_name}' exists on PyPI but its name is suspiciously close to "
                f"'{suggested}'. Manually verify this is the package you intended to install."
            ),
        }

    # Zafiyet var
    vuln_count = vuln_result.get("count", 0)
    if vuln_count > 0:
        latest = metadata.get("latest_version")
        return {
            "action": "UPGRADE",
            "message": (
                f"'{package_name}' has {vuln_count} known vulnerability(ies) in the "
                f"specified version. Consider upgrading to the latest version: {latest}"
            ),
        }

    # Hiçbir sorun yok
    return {
        "action": "NONE",
        "message": f"'{package_name}' shows no significant risk signals.",
    }