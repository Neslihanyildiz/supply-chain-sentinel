from datetime import datetime, timezone


def calculate_risk_score(metadata, typosquat_result, vuln_result):
    """
    Üç farklı analiz modülünün çıktısını birleştirip
    0-100 arası bir risk skoru ve kategori üretir.
    """
    score = 0
    reasons = []

    # 1. Paket PyPI'de hiç bulunamadıysa -> çok yüksek risk
    if not metadata.get("found", True):
        score += 40
        reasons.append("Package not found on PyPI (possible typo or removed/malicious package).")

    # 2. Typosquat şüphesi
    if typosquat_result.get("is_suspicious"):
        distance = typosquat_result.get("distance", 0)
        typosquat_score = 35 if distance == 1 else 25
        score += typosquat_score
        reasons.append(typosquat_result["reason"])

    # 3. Bilinen zafiyetler (sayı + CVSS ciddiyeti birlikte değerlendirilir)
    vuln_count = vuln_result.get("count", 0)
    if vuln_count > 0:
        vuln_score = min(vuln_count * 5, 30)
        score += vuln_score
        reasons.append(f"{vuln_count} known vulnerability(ies) found (OSV.dev).")

        max_cvss = vuln_result.get("max_cvss")

        if max_cvss is not None:
            if max_cvss >= 9.0:
                score += 15
                reasons.append(f"At least one vulnerability has a confirmed CVSS Base Score of {max_cvss}.")
            elif max_cvss >= 7.0:
                score += 8
                reasons.append(f"At least one vulnerability has a confirmed CVSS Base Score of {max_cvss}.")

    # 4. Paket çok yeni yayınlanmışsa -> ek risk sinyali
    # Mantık: saldırganlar genelde paketi yayınlayıp çok kısa süre içinde
    # popüler bir paket adına benzeterek yaymaya çalışır. "Yeni + şüpheli
    # isim" kombinasyonu, tek başına "yeni" olmaktan çok daha güçlü bir sinyal.
    first_release = metadata.get("first_release")
    if first_release:
        try:
            release_date = datetime.fromisoformat(first_release.replace("Z", "+00:00"))
            if release_date.tzinfo is None:
                release_date = release_date.replace(tzinfo=timezone.utc)
            days_since_release = (datetime.now(timezone.utc) - release_date).days

            if days_since_release <= 30:
                score += 20
                reasons.append(f"Package was first published only {days_since_release} day(s) ago.")
        except (ValueError, TypeError):
            # tarih formatı beklenmedikse sessizce atla, bu sinyali kullanma
            pass

    score = min(score, 100)

    if score >= 70:
        category = "CRITICAL"
    elif score >= 45:
        category = "HIGH"
    elif score >= 20:
        category = "MEDIUM"
    else:
        category = "LOW"

    return {
        "score": score,
        "category": category,
        "reasons": reasons if reasons else ["No significant risk signals detected."],
    }