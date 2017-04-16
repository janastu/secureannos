import subprocess
import json

anno = """
{
  "@context": "http://www.w3.org/ns/anno.jsonld",
  "id": "http://example.org/anno1",
  "type": "Annotation",
  "body": "Secret Annotation",
  "target": "file://./abc.pdf"
}
"""

def test():
    print("Testing encryption with anno: {}".format(anno))
    proc = subprocess.run(["python", "main.py", "-p", "abcdef", anno], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    print("Got encrypted annotation: {}".format(proc.stdout))
    print("Decrypting annotation")
    dproc = subprocess.run(["python", "main.py", "-d", "-p", "abcdef", proc.stdout], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    print("Decrypted annotation: {}".format(dproc.stdout))
    # ASSERTION
    print("Test successful: {}".format(json.loads(anno)['body'] == json.loads(dproc.stdout.decode('utf-8'))['body']))
    
    print("Attempting decryption with wrong password")
    dproc = subprocess.run(["python", "main.py", "-d", "-p", "abcdefg", proc.stdout], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Process result: {}".format(dproc.stderr))
    print("Attempting decryption with wrong target")
    wrong_anno = json.loads(proc.stdout.decode('utf-8'))
    wrong_anno['target'] = "file://./def.png"
    dproc = subprocess.run(["python", "main.py", "-d", "-p", "abcdef", json.dumps(wrong_anno)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Process result: {}".format(dproc.stderr))

if __name__ == '__main__':
    test()
