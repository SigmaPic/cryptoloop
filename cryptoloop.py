#!/usr/local/bin/python2.7
# encoding: utf-8
'''
cryptoloop -- A cryptoloop implementation in python with AES CBC
@author: SigmaPic
'''

from Crypto.Cipher import AES
import binascii
import struct

class AESCipher:
    SECTOR_SIZE = 512
    
    def __init__(self, key):
        self.key = key
    
    def decrypt_file(self, filename, out_file):
        self.transfer(filename, out_file, self.decrypt_sector)
        
    def encrypt_file(self, filename, out_file):
        self.transfer(filename, out_file, self.encrypt_sector)
    
    def transfer(self, filename, out_file, transfer_func):
        sector_id = 0
        
        with open(filename, "rb") as f:
            with open(out_file, "wb") as out:
                
                while True:
                    sector_data = f.read(AESCipher.SECTOR_SIZE)
                    
                    if len(sector_data) != AESCipher.SECTOR_SIZE:
                        break

                    out.write(transfer_func(sector_data, sector_id))
                    
                    sector_id += 1
        
    def decrypt_sector(self, sector_data, sector_id):
        iv = struct.pack("<I", sector_id) + b'\0' * 12
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return cipher.decrypt(sector_data)
    
    def encrypt_sector(self, sector_data, sector_id):
        iv = struct.pack("<I", sector_id) + b'\0' * 12
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return cipher.encrypt(sector_data)

def main(argv=None):
    
    import sys
    from argparse import ArgumentParser
    from argparse import RawDescriptionHelpFormatter
    
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_shortdesc = 'A cryptoloop implementation in python with AES CBC'

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_shortdesc, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-e", "--encrypt", dest="encrypt", action="store_true", help="Encrypt file", default=False)
        parser.add_argument("-d", "--decrypt", dest="decrypt", action="store_true", help="Decrypt file", default=False)
        parser.add_argument(dest="key", help="AES 128-bits key as hex string", metavar="key", nargs=1)
        parser.add_argument(dest="in_file", help="paths to input file", metavar="input", nargs=1)
        parser.add_argument(dest="out_file", help="paths to output file", metavar="output", nargs=1)

        # Process arguments
        args = parser.parse_args()

        encrypt = args.encrypt
        decrypt = args.decrypt
        key = args.key[0]
        in_file = args.in_file[0]
        out_file = args.out_file[0]
        
        if encrypt is True and decrypt is True:
            raise Exception('Chose either encrypt or decrypt but not both')
        
        aes = AESCipher(binascii.unhexlify(key))
        
        if decrypt is True:
            aes.decrypt_file(in_file, out_file)
        
        if encrypt is True:
            aes.encrypt_file(in_file, out_file)

        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        indent = len('cryptoloop') * " "
        sys.stderr.write('cryptoloop' + ": " + str(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    import sys
    sys.exit(main())