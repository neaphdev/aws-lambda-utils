import json
from jwcrypto import jwk, jwe
import time
import config as cfg
class MessageLevelEncription:

    def encrypt_yp(self, payload):
        payload = json.dumps(payload)
        protected_header = {
            "alg": "RSA-OAEP-256",
            "enc": "A128GCM",
            #"kid": cfg.keyid_yp,
            "iat": int(round(time.time() * 1000))
        }
        jwetoken = jwe.JWE(payload.encode('utf-8'),
                            recipient=self.loadPem("mle/keys/yp/publicKeyyp.pem"),
                            protected=protected_header)
        encryptedPayload = jwetoken.serialize(compact=True)
        return encryptedPayload

    def to_json(self, data):
        if type(data) == dict:
            return data
        return self.to_json(json.loads(data))

    def decrypt_pdp(self, dataencrypt):
        jwetoken = jwe.JWE()
        jwetoken.deserialize(dataencrypt, key=self.loadPem("mle/keys/pdp/privateKeypdp.pem"))
        kid_jwe = json.loads(jwetoken.objects["protected"])["kid"]
        return self.to_json(jwetoken.payload) 
        
    def loadPem(self, filePath):
        with open(filePath, "rb") as pemfile:
            return jwk.JWK.from_pem(pemfile.read())