# cryptoloop
A cryptoloop implementation in python with AES CBC.

This module allows:
- decrypting containers encrypted with cryptoloop
- encrypting containers like cryptoloop

cryptoloop encryption and decryption is always done on independent 512-bytes sectors.
IV (initial vector) of each sector is simply the sector id (starting from 0 for first sector).

# Usage
usage: cryptoloop.py [-h] [-e] [-d] key input output

A cryptoloop implementation in python with AES CBC

positional arguments:
  key            AES 128-bits key as hex string
  input          paths to input file
  output         paths to output file

optional arguments:
  -h, --help     show this help message and exit
  -e, --encrypt  Encrypt file
  -d, --decrypt  Decrypt file