# About
This is a Proof Of Concept - encrypting annotation bodies using a password and context(target) information.

# Usage

Given a simple annotation of the form

    {
          "@context": "http://www.w3.org/ns/anno.jsonld",
          "id": "http://example.org/anno1",
          "type": "Annotation",
          "body": "Secret Annotation",
          "target": "file://./abc.pdf"
    }

This program will encrypt the "body" and produce a base64 encoded encrypted body such as

    {
          "@context": "http://www.w3.org/ns/anno.jsonld",
          "id": "http://example.org/anno1",
          "type": "Annotation",
          "body": "WkqnguxUU0uUSfc8zI2sx4+fu4+W6SwW2EBtZ73F/TvGDjydaYSrMhiHIyzbnA==",
          "target": "file://./abc.pdf"
    }

This encrypted annotation can be shared with anyone. Only if the recipient has both the password used to encrypt as well as the file mentioned in the "target" of the annotation will they be able to decrypt the body and view the annotation. If the password is wrong or if the file mentioned in the target is either not present or is different even slightly the decryption will fail.

# Install
This program uses python3 (might work with python2 not tested). Use of [virtualenv](https://virtualenv.pypa.io/en/stable/) is recommended. To install the required libraries use:

    $ pip install -r requirements.txt

# Run

To encrypt an annotation:

    $ python -p mysuperpassword '{ "@context": "http://www.w3.org/ns/anno.jsonld", "target": "file://./abc.pdf", "body": "Secret annotation" }'

(encryption is the default operation)

To decrypt the annotation:
  
    $ python -p mysuperpassword '{ "@context": "http://www.w3.org/ns/anno.jsonld", "target": "file://./abc.pdf", "body": "WkqnguxUU0uUSfc8zI2sx4+fu4+W6SwW2EBtZ73F/TvGDjydaYSrMhiHIyzbnA==" }

# Tests

Simple test has been written without using python standard unittest framework. To see how to run the program and how to test/validate look at tests.py. To run the tests:

    $ python tests.py
