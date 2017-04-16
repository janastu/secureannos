#!/usr/bin/env python
#-*- coding: utf-8 -*-

from nacl import pwhash, secret, utils
import nacl.hash
import json
import sys
import base64
import argparse

def _get_salt(anno):
    target = anno['target']
    target_file = target.split("file://")[1]
    with open(target_file, "rb") as f:
        salt = nacl.hash.generichash(f.read(), digest_size=16)
    return salt

def encrypt(anno, password):
    anno = json.loads(anno)
    salt = _get_salt(anno)
    key = pwhash.kdf_scryptsalsa208sha256(secret.SecretBox.KEY_SIZE, password, salt, opslimit=pwhash.SCRYPT_OPSLIMIT_SENSITIVE, memlimit=pwhash.SCRYPT_MEMLIMIT_SENSITIVE)
    box = secret.SecretBox(key)
    anno['body'] = base64.b64encode(box.encrypt(str.encode(anno['body']))).decode('utf-8')

    return json.dumps(anno)

def decrypt(anno, password):
    anno = json.loads(anno)
    salt = _get_salt(anno)
    key = pwhash.kdf_scryptsalsa208sha256(secret.SecretBox.KEY_SIZE, password, salt, opslimit=pwhash.SCRYPT_OPSLIMIT_SENSITIVE, memlimit=pwhash.SCRYPT_MEMLIMIT_SENSITIVE)
    box = secret.SecretBox(key)
    anno['body'] = box.decrypt(base64.b64decode(anno['body'])).decode("utf-8")

    return json.dumps(anno)

def main():
    parser = argparse.ArgumentParser(description="Encrypts and decrypts annotations using the provided password and context information")
    parser.add_argument('-e','--encrypt', dest='operation', action='store_const', const='e', default='e', help="Operation to perform")
    parser.add_argument('-d','--decrypt', dest='operation', action='store_const', const='d', default='e', help="Operation to perform defaults to encrypt")
    parser.add_argument('-p','--password', help="Password", required=True)
    parser.add_argument("annotation", help="Annotation to encrypt/decrypt")

    options = parser.parse_args()

    if options.operation == 'e':
        print(encrypt(options.annotation, options.password.encode('utf-8')))
    else:
        print(decrypt(options.annotation, options.password.encode('utf-8')))

if __name__ == '__main__':
    main()
