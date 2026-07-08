[app]
title = app
package.name = vulktool
package.domain = org.example
source.dir = .
source.include_exts = py,enc
version = 1.0
requirements = python3,kivy,pyjnius,android,requests,pycryptodome
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
entrypoint = start.py
pypi_mirror = https://pypi.tuna.tsinghua.edu.cn/simple

[buildozer]
log_level = 2
warn_on_root = 1
