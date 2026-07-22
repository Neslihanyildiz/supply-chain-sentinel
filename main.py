from src.parser import parse_requirements
from src.metadata_collector import collect_all_metadata
from src.metadata_collector import get_package_metadata

packages = parse_requirements("test_data/requirements_sample.txt")
metadata_results = collect_all_metadata(packages)

for m in metadata_results:
    print(m)
    print("---")


from src.typosquat_analyzer import check_typosquat

print("\n--- Typosquat Analysis ---")
test_names = ["requests", "reqeusts", "reqeusts2", "flaskk", "django", "numpyy", "banana", "expresss"]
for name in test_names:
    result = check_typosquat(name)
    print(f"{name}: {result}")


from src.vulnerability_analyzer import check_vulnerabilities

print("\n--- Vulnerability Analysis (version-aware) ---")
for pkg in packages:
    result = check_vulnerabilities(pkg["name"], version=pkg.get("version"))
    print(f"{pkg['name']} ({pkg.get('version')}): found={result['vulnerabilities_found']}, count={result.get('count', 'N/A')}")


from src.risk_scorer import calculate_risk_score

print("\n--- Risk Scoring ---")
for pkg in packages:
    meta = get_package_metadata(pkg["name"])
    typo = check_typosquat(pkg["name"])
    vuln = check_vulnerabilities(pkg["name"], version=pkg.get("version"))
    risk = calculate_risk_score(meta, typo, vuln)
    print(f"{pkg['name']}: {risk}")


from src.recommendation_engine import generate_recommendation

print("\n--- Recommendations ---")
for pkg in packages:
    meta = get_package_metadata(pkg["name"])
    typo = check_typosquat(pkg["name"])
    vuln = check_vulnerabilities(pkg["name"], version=pkg.get("version"))
    risk = calculate_risk_score(meta, typo, vuln)
    rec = generate_recommendation(pkg["name"], meta, typo, vuln, risk)
    print(f"{pkg['name']}: [{rec['action']}] {rec['message']}")


from src.sbom_generator import generate_sbom

print("\n--- SBOM Generation ---")
metadata_list = [get_package_metadata(pkg["name"]) for pkg in packages]
sbom_path = generate_sbom(packages, metadata_list)
print(f"SBOM generated at: {sbom_path}")

# CI/CD build gate: eğer herhangi bir paket CRITICAL veya HIGH
# risk kategorisindeyse, işlemi hata koduyla sonlandır.
import sys

high_risk_found = False
for pkg in packages:
    meta = get_package_metadata(pkg["name"])
    typo = check_typosquat(pkg["name"])
    vuln = check_vulnerabilities(pkg["name"], version=pkg.get("version"))
    risk = calculate_risk_score(meta, typo, vuln)
    if risk["category"] in ("CRITICAL", "HIGH"):
        high_risk_found = True
        print(f"[BLOCKING] {pkg['name']} flagged as {risk['category']}: {risk['reasons']}")

if high_risk_found:
    print("\nBuild failed: one or more dependencies exceed the acceptable risk threshold.")
    sys.exit(1)
else:
    print("\nAll dependencies passed the security check.")