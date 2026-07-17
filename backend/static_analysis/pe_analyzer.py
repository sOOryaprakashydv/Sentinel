"""
PE / DLL Static Analyzer (Section 18).

Uses `pefile` for full analysis. If pefile isn't installed the analyzer
still returns a minimal-but-honest result (file-level entropy, no crash)
so the pipeline keeps moving — matching the PRD's "remains functional even
when a dependency/API is unavailable" principle.
"""
from __future__ import annotations

from pathlib import Path

from backend.static_analysis.entropy import shannon_entropy

SUSPICIOUS_IMPORTS = {
    "VirtualAlloc", "VirtualProtect", "WriteProcessMemory", "CreateRemoteThread",
    "SetWindowsHookEx", "GetProcAddress", "LoadLibraryA", "URLDownloadToFileA",
    "WinExec", "ShellExecuteA", "IsDebuggerPresent", "CreateToolhelp32Snapshot",
    "RegSetValueExA", "InternetOpenA", "InternetReadFile", "CryptEncrypt",
}


def analyze_pe(file_path: str | Path) -> dict:
    path = Path(file_path)
    raw = path.read_bytes()
    file_entropy = shannon_entropy(raw)

    result = {
        "metadata": {},
        "sections": [],
        "imports": [],
        "exports": [],
        "resources": [],
        "certificate": None,
        "security_findings": [],
        "entropy": round(file_entropy, 3),
        "compiler": None,
        "is_packed": file_entropy > 7.2,
        "yara_matches": [],
    }

    try:
        import pefile
    except ImportError:
        result["security_findings"].append({
            "title": "Limited analysis",
            "severity": "info",
            "detail": "pefile is not installed; only whole-file entropy was computed. "
                      "Install pefile for full PE parsing.",
        })
        return result

    try:
        pe = pefile.PE(data=raw, fast_load=True)
        pe.parse_data_directories()

        result["metadata"] = {
            "machine": hex(pe.FILE_HEADER.Machine),
            "timestamp": pe.FILE_HEADER.TimeDateStamp,
            "subsystem": pe.OPTIONAL_HEADER.Subsystem,
            "entry_point": hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint),
            "image_base": hex(pe.OPTIONAL_HEADER.ImageBase),
            "is_dll": pe.is_dll(),
            "is_exe": pe.is_exe(),
        }

        packed_sections = 0
        for section in pe.sections:
            sec_entropy = section.get_entropy()
            name = section.Name.decode(errors="ignore").strip("\x00")
            if sec_entropy > 7.0:
                packed_sections += 1
            result["sections"].append({
                "name": name,
                "virtual_size": section.Misc_VirtualSize,
                "raw_size": section.SizeOfRawData,
                "entropy": round(sec_entropy, 3),
            })

        if packed_sections >= 1:
            result["is_packed"] = True
            result["security_findings"].append({
                "title": "High-entropy section(s) detected",
                "severity": "high",
                "detail": f"{packed_sections} section(s) with entropy > 7.0, consistent with "
                          f"packing or encryption.",
            })

        flagged_imports: list[str] = []
        if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                dll_name = entry.dll.decode(errors="ignore") if entry.dll else "unknown"
                funcs = []
                for imp in entry.imports:
                    fname = imp.name.decode(errors="ignore") if imp.name else f"ordinal_{imp.ordinal}"
                    funcs.append(fname)
                    if fname in SUSPICIOUS_IMPORTS:
                        flagged_imports.append(fname)
                result["imports"].append({"dll": dll_name, "functions": funcs})

        if flagged_imports:
            result["security_findings"].append({
                "title": "Suspicious API imports",
                "severity": "medium",
                "detail": f"Imports commonly seen in malicious behavior: {', '.join(sorted(set(flagged_imports)))}",
            })

        if hasattr(pe, "DIRECTORY_ENTRY_EXPORT"):
            for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
                if exp.name:
                    result["exports"].append(exp.name.decode(errors="ignore"))

        if hasattr(pe, "DIRECTORY_ENTRY_RESOURCE"):
            result["resources"] = [
                {"type": str(getattr(r.struct, "Id", "unknown"))}
                for r in pe.DIRECTORY_ENTRY_RESOURCE.entries
            ]

        if not pe.verify_checksum():
            result["security_findings"].append({
                "title": "Invalid PE checksum",
                "severity": "low",
                "detail": "The declared checksum does not match the computed checksum.",
            })

        pe.close()

    except Exception as exc:  # pefile raises broadly on malformed files — that's expected input here
        result["security_findings"].append({
            "title": "Malformed PE structure",
            "severity": "medium",
            "detail": f"Parser error while reading PE headers: {exc}. This can itself indicate "
                      f"a manually crafted or corrupted file.",
        })

    return result
