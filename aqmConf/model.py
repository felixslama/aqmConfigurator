from asyncio import subprocess
from random import randint
import subprocess
import sys
from OpenSSL import crypto, SSL
import codecs
import requests
import zipfile
import os
import shutil
import platformio
from urllib import request

class MainModel():
    def __init__(self, parent=None):
        self.baseURL = "https://github.com/felixslama/aqm"

    def submit(self, url, token):
        fullURL = f"{url}?otp={token}"
        print(f"Submitted {fullURL}")

    def download(self): # Note: latest folder needs to be deleted before downloading again
        #downloadplatformio = subprocess.run([sys.executable, "-m", "pip", "install", "platformio"],stdout=subprocess.PIPE)
        #print(downloadplatformio.stdout.decode('utf-8'))
        #print("postdl")
        try:
            shutil.rmtree("latest/")
            shutil.rmtree("release/")
        except:
            pass
        print("Starting Download of latest release")
        r = requests.get("https://api.github.com/repos/felixslama/aqm/releases/latest")
        print(r.json()["zipball_url"])
        dr = requests.get(r.json()["zipball_url"],allow_redirects=True)
        open("release.zip", 'wb').write(dr.content)
        print("Download finished")

        with zipfile.ZipFile("release.zip", "r") as zip_ref:
            zip_ref.extractall("release/")
        print("Extraction finished, deleting zip file")
        os.remove("release.zip")
        
        #search for release folder and rename it
        for file in os.listdir("release/"):
            if file.startswith("felixslama"):
                print("Found file: " + file)
                os.rename("release/" + file, "latest")
                os.removedirs("release/")
        print("Renaming finished")
    
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
        cert.set_serial_number(randint(1,1000000))
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
        os.remove("cert.der")
        os.remove("key.der")
    def build(self):
        print("Build")
        print(platformio.VERSION)
        try:
            #move cert files to include folder
            #print("move done")
            #build firmware
            #releasePath = 'latest\software'
            #configPath = 'latest\software\platformio.ini'
            releasePath = 'latest/software'
            configPath = 'latest/software/platformio.ini'
            if not os.path.isdir(releasePath + "/.pio"):
                print("No .pio folder found, building firmware")
                self.download()
                self.createCert()
                shutil.move(os.path.join("cert.h"), os.path.join("latest/software/include/", "cert.h"))
                shutil.move(os.path.join("key.h"), os.path.join("latest/software/include/", "key.h"))
                shutil.copy(os.path.join("Credentials.h"), os.path.join("latest/software/include/", "Credentials.h"))
                worker = subprocess.run(["platformio", "run", "-c", str(configPath), "-d", str(releasePath), "--target", "upload"], stdout=subprocess.PIPE)
            else:
                print("Found .pio folder, skipping build, flashing firmware")
                self.createCert()
                shutil.move(os.path.join("cert.h"), os.path.join("latest/software/include/", "cert.h"))
                shutil.move(os.path.join("key.h"), os.path.join("latest/software/include/", "key.h"))
                shutil.copy(os.path.join("Credentials.h"), os.path.join("latest/software/include/", "Credentials.h"))
                worker = subprocess.run(["platformio", "run", "-c", str(configPath), "-d", str(releasePath), "--target", "upload"], stdout=subprocess.PIPE)
            print(worker.stdout.decode('utf-8'))
        except Exception as e:
            print("Build failed")
            print(e)
            return False
        #shutil.rmtree("latest/") # delete release folder for next download