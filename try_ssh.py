import os
import logging

cert_pem = os.getenv('CERT_SSL', "").encode()
key_pem = os.getenv('KEY_SSL', "").encode()
    # Ensure the /tmp/ directory exists
os.makedirs("/tmp", exist_ok=True)
# Write the decoded content to temporary files
with open('/tmp/cert.pem', 'wb') as cert_file:
    cert_file.write(cert_pem)

with open('/tmp/key.pem', 'wb') as key_file:
    key_file.write(key_pem)
if os.access('/tmp/cert.pem', os.R_OK):
    print("You have read permission for /tmp/cert.pem.")
else:
    print("You do not have read permission for /tmp/cert.pem.")
if os.path.isfile('/tmp/cert.pem'):
    print("/tmp/cert.pem is a file and exists.")
else:
    print("/tmp/cert.pem is not a valid file or does not exist.")
print(cert_pem)