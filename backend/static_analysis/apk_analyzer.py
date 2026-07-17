"""Android APK Static Analyzer (Section 18). Uses Androguard when available,
otherwise falls back to inspecting the AndroidManifest.xml presence via
plain zipfile so the pipeline still returns useful structure info."""
from __future__ import annotations

import zipfile
from pathlib import Path

DANGEROUS_PERMISSIONS = {
    "android.permission.SEND_SMS", "android.permission.READ_SMS",
    "android.permission.RECEIVE_SMS", "android.permission.CALL_PHONE",
    "android.permission.READ_CONTACTS", "android.permission.RECORD_AUDIO",
    "android.permission.CAMERA", "android.permission.ACCESS_FINE_LOCATION",
    "android.permission.SYSTEM_ALERT_WINDOW", "android.permission.REQUEST_INSTALL_PACKAGES",
    "android.permission.BIND_DEVICE_ADMIN", "android.permission.READ_SMS",
}


def analyze_apk(file_path: str | Path) -> dict:
    path = Path(file_path)

    result = {
        "metadata": {},
        "sections": [],
        "imports": [],
        "exports": [],
        "resources": [],
        "permissions": [],
        "certificate": None,
        "security_findings": [],
        "entropy": None,
        "compiler": None,
        "is_packed": False,
        "yara_matches": [],
    }

    try:
        from androguard.core.apk import APK
    except ImportError:
        try:
            with zipfile.ZipFile(path) as z:
                names = z.namelist()
                result["metadata"] = {
                    "has_manifest": "AndroidManifest.xml" in names,
                    "has_dex": any(n.endswith(".dex") for n in names),
                    "entry_count": len(names),
                }
        except zipfile.BadZipFile:
            pass
        result["security_findings"].append({
            "title": "Limited analysis",
            "severity": "info",
            "detail": "androguard is not installed; only archive structure was inspected. "
                      "Install androguard for manifest/permission/certificate parsing.",
        })
        return result

    try:
        apk = APK(str(path))
        result["metadata"] = {
            "package": apk.get_package(),
            "app_name": apk.get_app_name(),
            "min_sdk": apk.get_min_sdk_version(),
            "target_sdk": apk.get_target_sdk_version(),
            "main_activity": apk.get_main_activity(),
        }

        permissions = apk.get_permissions()
        result["permissions"] = permissions

        flagged = sorted(set(permissions) & DANGEROUS_PERMISSIONS)
        if flagged:
            result["security_findings"].append({
                "title": "Dangerous permissions requested",
                "severity": "medium",
                "detail": f"Requests high-risk permissions: {', '.join(flagged)}",
            })

        if apk.is_signed_v1() or apk.is_signed_v2() or apk.is_signed_v3():
            certs = apk.get_certificates()
            if certs:
                cert = certs[0]
                result["certificate"] = {
                    "subject": str(cert.subject),
                    "issuer": str(cert.issuer),
                    "serial_number": str(cert.serial_number),
                }
        else:
            result["security_findings"].append({
                "title": "Unsigned APK",
                "severity": "high",
                "detail": "The APK is not signed, which is unusual for legitimately distributed apps.",
            })

        activities = apk.get_activities()
        services = apk.get_services()
        receivers = apk.get_receivers()
        result["exports"] = activities + services + receivers

        if apk.get_permissions().count("android.permission.REQUEST_INSTALL_PACKAGES"):
            result["security_findings"].append({
                "title": "Can install additional packages",
                "severity": "high",
                "detail": "This app can prompt installation of further APKs, a common dropper pattern.",
            })

    except Exception as exc:
        result["security_findings"].append({
            "title": "APK parsing error",
            "severity": "medium",
            "detail": f"Androguard failed to fully parse this APK: {exc}",
        })

    return result
