from asyncio import subprocess
import subprocess
from sys import stdout
from OpenSSL import crypto, SSL
import hexdump
import codecs
import requests
import zipfile
import os
import shutil
from urllib import request

class MainModel():
    def __init__(self, parent=None):
        self.baseURL = "https://github.com/felixslama/aqm"

    def check(self):
        print("Check")

    def download(self): # Note: latest folder needs to be deleted before downloading again
        #print("Starting Download of latest release")
        r = requests.get("https://api.github.com/repos/felixslama/aqm/releases/latest")
        #print(r.json()["zipball_url"])
        dr = requests.get(r.json()["zipball_url"],allow_redirects=True)
        open("release.zip", 'wb').write(dr.content)
        #print("Download finished")

        with zipfile.ZipFile("release.zip", "r") as zip_ref:
            zip_ref.extractall("release/")
        #print("Extraction finished, deleting zip file")
        os.remove("release.zip")
        
        #search for release folder and rename it
        for file in os.listdir("release/"):
            if file.startswith("felixslama"):
                #print("Found file: " + file)
                os.rename("release/" + file, "latest")
                os.removedirs("release/")
        #print("Renaming finished")
    
    def createCert(self):
        # this function creates a key and certificate for the esp32 webserver and saves it as usable .h file 
        # create a key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 2048)

        # create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = "AT"
        cert.get_subject().ST = "CA"
        cert.get_subject().L = "Villach"
        cert.get_subject().O = "AETHERENGINEERING"
        cert.get_subject().OU = "aqm"
        cert.get_subject().CN = "aqm"
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10*365*24*60*60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha256')

        # create cert in der format
        with open("cert.der", "wb") as f:
            f.write(
                crypto.dump_certificate(crypto.FILETYPE_ASN1, cert)
            )
        # create key in der format
        with open("key.der", "wb") as f:
            f.write(
                crypto.dump_privatekey(crypto.FILETYPE_ASN1, k)
            )

        #create c header file for cert
        cert_list = []
        with open('cert.der', 'rb') as f:
            for chunk in iter(lambda: f.read(1), b''):
                cert_list.append("0x" + codecs.encode(chunk, 'hex').decode("utf-8"))
            with open('cert.h', 'w') as tf:
                tf.write("unsigned char AQM_crt_DER[] = {\n")
                for i in range(0, len(cert_list)):
                    tf.write("\t" + cert_list[i] + ",\n")
                tf.write("};\n")
                tf.write("unsigned int AQM_crt_DER_len = " + str(len(cert_list)) + ";")
            
        #create c header file for key
        key_list = []
        with open('key.der', 'rb') as f:
            for chunk in iter(lambda: f.read(1), b''):
                key_list.append("0x" + codecs.encode(chunk, 'hex').decode("utf-8"))
            with open('key.h', 'w') as tf:
                tf.write("unsigned char AQM_key_DER[] = {\n")
                for i in range(0, len(key_list)):
                    tf.write("\t" + key_list[i] + ",\n")
                tf.write("};\n")
                tf.write("unsigned int AQM_key_DER_len = " + str(len(key_list)) + ";")

    def build(self):
        print("Build")
        self.download()
        self.createCert()
        #move cert files to include folder
        shutil.move("cert.h", "latest/software/include/")
        shutil.move("key.h", "latest/software/include/")
        shutil.copy("Credentials.h", "latest/software/include/")
        #build firmware
        releasePath = "latest/software"
        configPath = "latest/software/platformio.ini"
        #command = 'platformio run --environment esp32dev -d ' + workingDir + '-c ' + workingDir + '/platformio.ini'
        worker = subprocess.run(["platformio", "run", "-c", str(configPath), "-d", str(releasePath)], stdout=subprocess.PIPE)
        print(worker.stdout.decode('utf-8'))

        #os.removedirs("latest/") # delete release folder for next download