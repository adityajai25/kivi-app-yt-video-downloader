[app]

# (str) Title of your application
title = ezy downloader

# (str) Package name
package.name = ezy_downloader

# (str) Package domain (needed for android/ios packaging)
package.domain = org.ezy.downloader

# (str) Source code where the main.py live
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
requirements = python3,kivy,pytube,validators

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# The source directory of your Kivy project
source.dir = .

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# Static version number
version = 0.0.1

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE

# (list) Android architectures to build for
android.arch = armeabi-v7a, arm64-v8a

# (list) Services to declare
services = 

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Time before retrying to start the build process in case of failure (in seconds)
retry = 0

# (list) List of warnings to ignore (e.g. unused variable 'Token')
warn_on_unused_configs = True
