from ast import dump
from encodings import utf_8
from subprocess import Popen, PIPE, DEVNULL
from tokenize import String
from OpenSSL import crypto, SSL
import hexdump
import codecs
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
        #this function creates a key and certificate for the esp32 webserver and saves it as usable .h file 
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

        