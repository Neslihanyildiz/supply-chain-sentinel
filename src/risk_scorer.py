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
        # mesafe küçükse (1) daha yüksek puan, büyükse (2) biraz daha az
        typosquat_score = 35 if distance == 1 else 25
        score += typosquat_score
        reasons.append(typosquat_result["reason"])

    # 3. Bilinen zafiyetler
    vuln_count = vuln_result.get("count", 0)
    if vuln_count > 0:
        # zafiyet sayısı arttıkça puan artar ama belli bir tavanla sınırlı
        vuln_score = min(vuln_count * 5, 30)
        score += vuln_score
        reasons.append(f"{vuln_count} known vulnerability(ies) found (OSV.dev).")

    # 4. Paket çok yeni yayınlanmışsa (son 30 gün içinde ilk yayın) -> ek risk
    # Not: first_release string olarak geliyor, şimdilik basit tutuyoruz,
    # gerçek tarih karşılaştırması Gün 4'te eklenecek.

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