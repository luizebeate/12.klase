import hashlib
parole = 'Mēbeles'
parole_bin = str.encode(parole)
parole_hash = hashlib.md5(parole_bin)
parole_md5 = parole_hash.hexdigest()
print(parole_md5)