[app]

# (str) Naslov aplikacije
title = VizoX

# (str) Ime paketa (mora biti jedna reč, mala slova)
package.name = vizoxapp

# (str) Domen paketa
package.domain = org.vizox

# (str) Izvorna fascikla gde je main.py
source.dir = .

# (list) Ekstenzije fajlova koje se uključuju
source.include_exts = py,png,jpg,kv,atlas

# (str) Verzija aplikacije
version = 1.0

# (list) BIBLIOTEKE - DODATO: requests, certifi, urllib3 (KLJUČNO ZA IPTV)
requirements = python3,kivy,requests,certifi,urllib3,idna,charset-normalizer

# (list) Orijentacija - Promenjeno u landscape (položeno za TV/Video)
orientation = landscape

#
# Android specific
#

# (bool) Fullscreen mode
fullscreen = 1

# (list) PERMISIJE - OTKLJUČANO: Internet pristup
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (int) Target Android API (31 je standard za nove sisteme)
android.api = 31

# (int) Minimum API (21 omogućava rad i na starijim TV boksovima)
android.minapi = 21

# (bool) Automatsko prihvatanje licenci (Štedi vreme pri bildovanju)
android.accept_sdk_license = True

# (list) Arhitekture za koje se pravi APK
android.archs = arm64-v8a, armeabi-v7a

# (bool) Omogući backup
android.allow_backup = True

#
# Python for android (p4a) specific
#

# (str) Bootstrap koji se koristi
p4a.bootstrap = sdl2

[buildozer]

# (int) Log level (2 znači da ćeš videti sve detalje ako negde zapne)
log_level = 2

# (int) Upozorenje za root (0 isključuje dosadno pitanje)
warn_on_root = 0