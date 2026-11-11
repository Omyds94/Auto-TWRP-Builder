#!/usr/bin/env python3
"""Validate the stock Unisoc first-stage recovery module bundle."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MODULE_DIR = ROOT / "recovery" / "root" / "lib" / "modules"
LOAD_LIST = MODULE_DIR / "modules.load.recovery"
DEP_FILE = MODULE_DIR / "modules.dep"
REQUIRED = {
    "ufs_sprd.ko",
    "sprd-drm.ko",
    "sprd-gsp.ko",
    "himax_mmi_spi.ko",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def module_basename(path: str) -> str:
    name = Path(path.strip()).name
    if not name.endswith(".ko"):
        fail(f"unexpected module reference: {path!r}")
    return name


def main() -> int:
    if not MODULE_DIR.is_dir():
        fail(f"module directory missing: {MODULE_DIR}")
    if not LOAD_LIST.is_file() or not DEP_FILE.is_file():
        fail("modules.load.recovery or modules.dep is missing")

    load_entries = [
        line.strip()
        for line in LOAD_LIST.read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if len(load_entries) != len(set(load_entries)):
        fail("modules.load.recovery contains duplicate entries")

    missing_load = [name for name in load_entries if not (MODULE_DIR / name).is_file()]
    if missing_load:
        fail("files missing from recovery load list: " + ", ".join(missing_load))

    dep_map: dict[str, list[str]] = {}
    for number, line in enumerate(DEP_FILE.read_text().splitlines(), 1):
        if not line.strip():
            continue
        target, sep, deps = line.partition(":")
        if not sep:
            fail(f"malformed modules.dep line {number}")
        target_name = module_basename(target)
        dep_names = [module_basename(item) for item in deps.split()]
        if target_name in dep_map:
            fail(f"duplicate modules.dep target: {target_name}")
        dep_map[target_name] = dep_names

    missing_dep_files = []
    for target, deps in dep_map.items():
        if not (MODULE_DIR / target).is_file():
            missing_dep_files.append(target)
        for dep in deps:
            if not (MODULE_DIR / dep).is_file():
                missing_dep_files.append(f"{target} -> {dep}")
    if missing_dep_files:
        fail("missing dependency files: " + ", ".join(missing_dep_files))

    missing_dep_records = [name for name in REQUIRED if name not in dep_map]
    if missing_dep_records:
        fail("critical modules absent from modules.dep: " + ", ".join(sorted(missing_dep_records)))
    missing_required_load = REQUIRED.difference(load_entries)
    if missing_required_load:
        fail("critical modules absent from recovery load list: " + ", ".join(sorted(missing_required_load)))

    # Compute and validate the transitive dependency closure for critical drivers.
    closure: set[str] = set()
    visiting: set[str] = set()

    def visit(name: str) -> None:
        if name in closure:
            return
        if name in visiting:
            fail(f"dependency cycle detected at {name}")
        visiting.add(name)
        for dep in dep_map.get(name, []):
            visit(dep)
        visiting.remove(name)
        closure.add(name)

    for name in REQUIRED:
        visit(name)

    missing_from_load = sorted(closure.difference(load_entries))
    if missing_from_load:
        fail("critical dependency closure not covered by recovery load list: " + ", ".join(missing_from_load))

    print("PASS: stock recovery module bundle is internally consistent")
    print(f"  recovery load-list entries : {len(load_entries)}")
    print(f"  modules.dep records        : {len(dep_map)}")
    print(f"  critical modules           : {', '.join(sorted(REQUIRED))}")
    print(f"  critical dependency closure: {len(closure)} files present and listed")
    print("  vermagic / symbol CRC runtime compatibility is not tested by this script")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
