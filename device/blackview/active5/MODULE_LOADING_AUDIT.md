# First-stage recovery module loading audit

## Device evidence

- Running kernel: `5.15.149-android13-8-00008-gbe074b05e5af-ab12096863`.
- Kernel config: `CONFIG_MODVERSIONS=y`; `CONFIG_MODULE_FORCE_LOAD` and
  `CONFIG_MODULE_SIG_FORCE` are disabled.
- `/proc/modules` showed `ufs_sprd`, `rpmb`, `sprd_soc_id`, `sprd_drm`,
  `sprd_gsp`, `himax_mmi_spi` and `ilitek_spi` loaded in Android.
- Module taints shown by sysfs were `E` for UFS/RPMB/SoC ID and `OE` for
  DRM/GSP/Himax. This does not indicate forced loading.

## Stock ramdisk module bundle

The device tree contains 153 entries in `modules.load.recovery` and 153
`modules.dep` records. All listed `.ko` files exist, all dependency references
resolve, and the critical module dependency closure is covered by the recovery
load list. The UFS chain is:

`ufs_sprd.ko` -> `sprd_soc_id.ko`, `rpmb.ko`, `sprd_sip_svc.ko`, `sysdump.ko`.

SHA-256 comparisons confirmed that those five files match the original
vendor_boot-derived tree. The Himax, Ilitek, DRM and GSP files also match the
live `vendor_dlkm` extraction.

## Loading mechanism

The selected TWRP 14.1 `system/core/init/first_stage_init.cpp` chooses
`modules.load.recovery` in recovery mode (falling back to `modules.load` only
when the recovery list is absent) and loads the list from `/lib/modules`.
This occurs in first-stage init before first-stage mounts. Accordingly, this
tree keeps the stock list and dependency metadata intact and does not enable
the later TWRP userspace `TW_LOAD_VENDOR_MODULES` loader.

The host-side audit script checks only file/list/dependency consistency. It
does not prove kernel symbol CRC compatibility or successful operation in a
TWRP runtime; those still require a booted recovery test.
