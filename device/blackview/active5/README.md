# TWRP Device Tree for blackview active5

This tree was generated from a stock Android 15
Unisoc `vendor_boot` image. Build it with the `twrp-14.1`
source branch and lunch target `twrp_active5-ap2a-eng`.

The stock DTB, first-stage fstab, kernel modules, recovery init/ueventd files,
SELinux policy and context files are retained under `recovery/root` and copied
to `vendor_ramdisk`. The supplied vendor_boot contains no vendor subtree, so
KeyMint/Trusty libraries must be obtained by mounting the actual logical
`/vendor` partition; the device configuration uses `TW_USES_VENDOR_LIBS`.
The generated image is `vendor_boot.img`; keep the stock `boot.img` in place.

`prebuilt/sourcecode` contains the source overlay required for decryption.
Run `./patch.sh` from that directory before building; it backs up each replaced
source file to `original`. Run `./recovery.sh` to restore those originals.

This tree carries the stock vendor SELinux policy and includes a manual helper
under `tools/` to mark `init` and `recovery` permissive. The device makefiles do
not invoke this helper automatically. For a deliberate local policy rebuild,
compile the C helper against static `libsepol`, set `SEPOLICY_PATCHER` to the
resulting executable, and run `tools/patch_stock_sepolicy.sh`. No custom
`recovery.te` overlay is included because the generator template was absent.
This device uses the SC27XX input vibrator overlay.
This platform also includes the UMS9620/UMS9230 legacy DRM modeset overlay.
The vendor ramdisk exposes a Himax touchscreen module. The branch-neutral
Himax `minuitwrp/events.cpp` touch-release overlay is included.

## Recovery kernel-module loading

The full stock module directory is preserved at `recovery/root/lib/modules`,
including `modules.dep`, `modules.alias`, `modules.softdep`, and
`modules.load.recovery`. Android first-stage init in the TWRP 14.1 source tree
selects `modules.load.recovery` when booting in recovery mode and loads the
listed modules from `/lib/modules` before first-stage partition mounts. This is
critical for the UFS controller and the dynamic-partition mount sequence.

The retained recovery list has 153 unique entries. A local audit confirms that
every listed `.ko` exists and every dependency named by `modules.dep` resolves
to a file in the same directory. The list and dependency map should not be
trimmed or regenerated from `vendor_dlkm`: this is the stock vendor-ramdisk
recovery module set. `TW_LOAD_VENDOR_MODULES` is intentionally not enabled;
TWRP's userspace module loader is later in startup and is unnecessary when
first-stage init has already loaded the recovery list.

Run `python3 tools/audit_recovery_modules.py` from this device-tree directory
before building to repeat the file/dependency checks.
