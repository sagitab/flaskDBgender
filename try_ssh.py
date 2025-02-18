import os 

cert_pem = os.getenv('CERT_SSL', "").encode()
try:
      # Ensure the /tmp/ directory exists
    os.makedirs("/tmp", exist_ok=True)
    # Write the decoded content to temporary files
    with open('/tmp/cert.pem', 'wb') as cert_file:
        cert_file.write(cert_pem)
        print("ok")
except Exception as e:
    print("fail")
    print(str(e))  # Correct way to print the error message