import codecs
import requests
import zipfile
import os
import shutil
import requests
import json
import subprocess
from asyncio import subprocess
from random import randint
from OpenSSL import crypto

class MainModel():
    def __init__(self, parent=None):
        self.base_URL = "https://github.com/felixslama/aqm"
        self.base_fetch_URL = "https://aqmcredman.azurewebsites.net/api/aqmcredman"
        self.base_release_path = "latest/software/"
        self.release_URL = "https://api.github.com/repos/felixslama/aqm/releases/latest"
    
    def submit(self, token):
        full_URL = f"{self.base_fetch_URL}?otp={token}"
        response = requests.get(full_URL)
        # if API-Fetch was a Success, write to Header File
        if response.status_code == 200:
            json_creds = f"{response.json()}"
            # replace with double quotes because json lib doesnt like single quotes
            json_creds = json_creds.replace("'", '"')
            decoded_json = json.loads(json_creds)
            # delete previous Header File
            if os.path.isfile("Credentials.h"):
                os.remove("Credentials.h")
            with open("Credentials.h", "w") as f:
                for k, v in decoded_json.items():
                    f.write(f"const char* {k} = {v};\n")
                f.close()
            return True
        else:
            print(f"Error: {response.status_code}")
            return False
    
    def download(self):
        try:
            shutil.rmtree("latest/")
            shutil.rmtree("release/")
        except:
            pass
        response = requests.get(f"{self.release_URL}")
        download_request = requests.get(response.json()["zipball_url"],allow_redirects=True)
        open("release.zip", 'wb').write(download_request.content)
        with zipfile.ZipFile("release.zip", "r") as zip_ref:
            zip_ref.extractall("release/")
        os.remove("release.zip")
        #search for release folder and rename it
        for file in os.listdir("release/"):
            if file.startswith("felixslama"):
                print("Found file: " + file)
                os.rename("release/" + file, "latest")
                os.removedirs("release/")
    
    def createCert(self):
        # create a Key Pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 2048)
        # create a self-signed Cert
        cert = crypto.X509()
        cert.get_subject().C = "AT"
        cert.get_subject().ST = "CA"
        cert.get_subject().L = "Villach"
        cert.get_subject().O = "AETHERENGINEERING"
        cert.get_subject().OU = "aqm"
        cert.get_subject().CN = "aqm"
        cert.set_serial_number(randint(1,1000000))
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10*365*24*60*60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha256')
        # create Cert in der-Format
        with open("cert.der", "wb") as f:
            f.write(
                crypto.dump_certificate(crypto.FILETYPE_ASN1, cert)
            )
            f.close()
        # create Key in der-Format
        with open("key.der", "wb") as f:
            f.write(
                crypto.dump_privatekey(crypto.FILETYPE_ASN1, k)
            )
            f.close()
        # create Header File for Cert
        cert_list = []
        with open('cert.der', 'rb') as f:
            for chunk in iter(lambda: f.read(1), b''):
                cert_list.append("0x" + codecs.encode(chunk, 'hex').decode("utf-8"))
            with open('cert.h', 'w') as cf:
                cf.write("unsigned char AQM_crt_DER[] = {\n")
                for i in range(0, len(cert_list)):
                    cf.write("\t" + cert_list[i] + ",\n")
                cf.write("};\n")
                cf.write("unsigned int AQM_crt_DER_len = " + str(len(cert_list)) + ";")
                cf.close()
            f.close()
        # create Header File for Key
        key_list = []
        with open('key.der', 'rb') as f:
            for chunk in iter(lambda: f.read(1), b''):
                key_list.append("0x" + codecs.encode(chunk, 'hex').decode("utf-8"))
            with open('key.h', 'w') as kf:
                kf.write("unsigned char AQM_key_DER[] = {\n")
                for i in range(0, len(key_list)):
                    kf.write("\t" + key_list[i] + ",\n")
                kf.write("};\n")
                kf.write("unsigned int AQM_key_DER_len = " + str(len(key_list)) + ";")
                kf.close()
            f.close()
        os.remove("cert.der")
        os.remove("key.der")
    
    def build(self):
        try:
            configPath = f"{self.base_release_path}platformio.ini"
            if not os.path.isdir(self.base_release_path + ".pio"):
                self.download()
                self.createCert()
                shutil.move(os.path.join("cert.h"), os.path.join(f"{self.base_release_path}include/", "cert.h"))
                shutil.move(os.path.join("key.h"), os.path.join(f"{self.base_release_path}include/", "key.h"))
                shutil.copy(os.path.join("Credentials.h"), os.path.join(f"{self.base_release_path}include/", "Credentials.h"))
                worker = subprocess.run([
                    "platformio", "run", 
                    "-c", configPath, 
                    "-d", self.base_release_path, 
                    "--target", "upload"
                    ],stdout=subprocess.PIPE)
            else:
                self.createCert()
                shutil.move(os.path.join("cert.h"), os.path.join(f"{self.base_release_path}include/", "cert.h"))
                shutil.move(os.path.join("key.h"), os.path.join(f"{self.base_release_path}include/", "key.h"))
                shutil.copy(os.path.join("Credentials.h"), os.path.join(f"{self.base_release_path}include/", "Credentials.h"))
                worker = subprocess.run(
                    [
                    "platformio", "run", 
                    "-c", configPath,
                    "-d", self.base_release_path, 
                    "--target", "upload"
                    ],stdout=subprocess.PIPE)
            print(worker.stdout.decode('utf-8'))
        except Exception as e:
            print("Build failed")
            print(e)
            return False
