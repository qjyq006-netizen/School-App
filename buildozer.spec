[app]
title = School Management Smart System
package.name = schoolapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,kivymd,arabic_reshaper,python-bidi
orientation = portrait
osx.kivy_version = 2.1.0
fullscreen = 0
android.archs = armeabi-v7a, arm64-v8a
android.allow_backup = True
android.api = 33
android.minapi = 24
android.ndk_api = 21
android.private_storage = True

[buildozer]
log_level = 2
warn_on_root = 1
