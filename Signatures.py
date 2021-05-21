# Digital signatures
# Type: Asymmetric encryption --> RSA
#   RSA: generates two keys; private and public.

# Note: encryption function requires byte (i.e. type(b'message')) type not str
# you can use byte(string,'utf-8') to convert string to bytes

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_keys():
    private = rsa.generate_private_key(
        key_size= 2048, 
        public_exponent= 65537,
        backend= default_backend()
    )
    public = private.public_key()
    pu_ser = public.public_bytes(
       encoding=serialization.Encoding.PEM,
       format=serialization.PublicFormat.SubjectPublicKeyInfo
     )
    
    return private,pu_ser

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def sign(message, private):
    sig = private.sign(
        message,
        padding.PSS(
            mgf = padding.MGF1(hashes.SHA256()),
            salt_length = padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return sig

from cryptography.exceptions import InvalidSignature
def verify(message, sig, pu_ser):
    public = serialization.load_pem_public_key(
        pu_ser,
        backend = default_backend()
    )
    try:
        public.verify(
            sig,
            message,
            padding.PSS(
                mgf = padding.MGF1(hashes.SHA256()),
                salt_length = padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False
    except:
        print('Error executing public_key.verify')
        return False


if __name__ == '__main__':
    pr,pu = generate_keys()
    message = b'This is a secret message'
    sig = sign(message, pr)
    correct = verify(message,sig,pu)
    print(correct)
    
    if correct:
        print('Success! Good sign')
        
    else:
        print('Error: signature is bad')
        
    ## Lets pretend to sign someone else using my private and their public key
    pr2,pu2 = generate_keys()
    sig2 = sign(message,pr2)
    corr = verify(message, sig2, pu)
    if corr:
        print('Error! Bad signature checks out')
    else:
        print('Success! Bad sig detected')
        
#     tempering with the message
    badmessage = message + b'Q'
    correct = verify(badmessage,sig,pu)
    if correct:
        print('Error! Tempered message checks out')
        
    else:
        print('Success! Tempering detected')