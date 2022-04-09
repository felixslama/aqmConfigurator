from ast import dump
from encodings import utf_8
from subprocess import Popen, PIPE, DEVNULL
from OpenSSL import crypto, SSL
import hexdump
from urllib import request

class MainModel():
    def __init__(self, parent=None):
        self.baseURL = "https://github.com/felixslama/aqm"

    def build(self, configPath, releasePath):
        print("Build")
        #process = Popen(["platformio", "run", "-c", str(configPath), "-d", str(releasePath)], stdout=PIPE, stderr=PIPE, stdin=DEVNULL,)
        #(out, err) = process.communicate()

    def check(self):
        print("Check")

    def download(self):
        print("Check")
    
    def createCert(self):
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
        # write cert to file
        with open("cert.pem", "wt") as f:
            f.write(
                crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode('utf-8')
            )

        # write private key to file
        with open("key.pem", "wt") as f:
            f.write(
                crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode('utf-8')
            )
        # convert certificate to der format
        with open("cert.der", "wb") as f:
            f.write(
                crypto.dump_certificate(crypto.FILETYPE_ASN1, cert)
            )
        # convert private key to der format
        with open("key.der", "wb") as f:
            f.write(
                crypto.dump_privatekey(crypto.FILETYPE_ASN1, k)
            )
        # print certificate with hexdump
        print(hexdump.hexdump(open("cert.der", "rb").read()))
        # print private key with hexdump
        print(hexdump.hexdump(open("key.der", "rb").read())
        