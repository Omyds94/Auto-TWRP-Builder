# Active 5 TWRP tree — reviewed changes (pre-build)

This revision is a conservative device-specific correction pass over the uploaded
`active5.zip`. It is **not a compiled or boot-tested recovery**.

## Changes made

1. Replaced the generated `twrp.fstab` and fallback `recovery.fstab` with entries
   matching the confirmed UFS by-name names and A/B layout. Removed the inherited
   eMMC/SPL, modem, SD-card and NV entries that were not supported by the supplied
   Active 5 partition map. Kept only EROFS variants for logical partitions and
   F2FS for `/data`, `/metadata` and `/cache`.
2. Preserved the stock `/data` encryption string and `keydirectory` in TWRP flags.
   The metadata-encryption path still requires a real-device functional test; this
   file does not claim that decryption is already working.
3. Removed the stock recovery init actions that write to `mmcblk0boot0/1` and start
   the eMMC/SPL helper. The other Unisoc health, USB and power actions were retained.
4. Added 800x1340 display dimensions from the handset's previously supplied kernel
   diagnostics.
5. Removed `TW_EMBEDDED_VENDOR_LIBS := true`, because the uploaded device tree has
   an empty `recovery/root/vendor` directory. Set `TW_USES_VENDOR_LIBS := true` so
   the actual logical `/vendor` can be mounted for KeyMint/vendor libraries.
6. Audited all 153 entries in the stock `modules.load.recovery` list and all
   153 records in `modules.dep`: every listed module and every dependency file
   exists in `recovery/root/lib/modules`. The recovery list includes `ufs_sprd`,
   `sprd-drm`, `sprd-gsp` and `himax_mmi_spi`, as well as the UFS dependencies.
7. Removed the redundant TWRP userspace `TW_LOAD_VENDOR_MODULES` loader flags.
   TWRP 14.1's `system/core/init/first_stage_init.cpp` selects
   `modules.load.recovery` in recovery mode and loads it from `/lib/modules`
   before first-stage partition mounts. This is the required early mechanism
   for UFS and dynamic partitions. The stock ramdisk module list/dependency
   files are preserved unchanged.
8. Compared SHA-256 values for the recovery-critical modules. The UFS module
   and four UFS dependencies match the original generated tree; the Himax,
   Ilitek, DRM and GSP modules match both the original tree and the live
   `vendor_dlkm` extraction.

## Deliberately not changed / outstanding

- No `recovery.te` was invented. The generator's `sprd_recovery.te.jinja2`
  template is absent. The stock policy files remain byte-identical to each other.
- The generated `init.custom.rc` still requests permissive SELinux for recovery.
  The policy/helper approach must be reviewed before a release build.
- The generator's stock-policy helper is not invoked by the device makefiles in
  this tree; treat it as a manual helper, not an automatic build step.
- FBE metadata decryption needs validation on the device. `TW_INCLUDE_CRYPTO := true`
  in the carried TWRP 14.1 `Android.mk` enables `USE_FSCRYPT` and
  `TW_INCLUDE_FBE_METADATA_DECRYPT`; this is a positive compile-time condition,
  not proof that KeyMint/Trusty runtime decryption succeeds.
- First-stage module loading is based on the retained stock `modules.load.recovery`
  file. The module `vermagic` release field differs from `uname -r`, but
  `CONFIG_MODVERSIONS=y` means Linux 5.15 compares the remaining vermagic flags
  and validates symbol CRCs. No forced module-loading flag is configured.
  Successful Android loading and the absence of matching module-load errors
  in the supplied `dmesg` excerpt are encouraging, but do not prove the TWRP
  environment will have identical symbol exports.
- Verify both FSTAB files against the live by-name list before building.
- Verify the `vendor_boot` image size remains within the 104857600-byte partition.

## Safety

Do not flash this tree or an image generated from it yet. Do not flash `vbmeta`,
`boot`, `init_boot`, `dtbo` or `vendor_boot` until a build has been audited and
an explicit recovery path using the original slot images is ready.
