#
# Copyright (C) 2026 The Android Open Source Project
# Copyright (C) 2026 SebaUbuntu's TWRP device tree generator
#
# SPDX-License-Identifier: Apache-2.0
#

$(call inherit-product, $(SRC_TARGET_DIR)/product/aosp_base.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit.mk)
$(call inherit-product-if-exists, $(SRC_TARGET_DIR)/product/gsi_keys.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)
$(call inherit-product-if-exists, vendor/twrp/config/common.mk)

$(call inherit-product, device/blackview/active5/device.mk)

PRODUCT_DEVICE := active5
PRODUCT_NAME := twrp_active5
PRODUCT_BRAND := Blackview
PRODUCT_MODEL := Active 5
PRODUCT_MANUFACTURER := blackview
PRODUCT_RELEASE_NAME := active5

PRODUCT_BUILD_PROP_OVERRIDES += \
    PRIVATE_BUILD_DESC="Active_5_NEU-user 15 AP3A.240905.015.A2 20250628 release-keys"
BUILD_FINGERPRINT := Blackview/Active_5_NEU/Active_5:15/AP3A.240905.015.A2/20250628:user/release-keys
