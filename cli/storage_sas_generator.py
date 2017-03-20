import base64
import hashlib
import hmac
from urllib import quote
from datetime import datetime, timedelta


SIGNED_PERMISSIONS = "sp"
SIGNED_SERVICE = "ss"
SIGNED_RESOURCE_TYPE = "srt"
SIGNED_IP = "sip"
SIGNED_EXPIRY = "se"
SIGNED_VERSION = "sv"
SIGNED_START = ""
SIGNED_PROTOCOL = ""
DAYS_TO_EXPIRY = 365 * 2


def encode_base64(data):
    if isinstance(data, unicode):
        data = data.encode('utf-8')
    encoded = base64.b64encode(data)
    return encoded.decode('utf-8')

def decode_base64_to_bytes(data):
    if isinstance(data, unicode):
        data = data.encode('utf-8')
    return base64.b64decode(data)

def decode_base64_to_text(data):
    decoded_bytes = decode_base64_to_bytes(data)
    return decoded_bytes.decode('utf-8')

def get_content_md5(data):
    md5 = hashlib.md5()
    md5.update(data)
    return base64.b64encode(md5.digest()).decode('utf-8')


class StorageSASGenerator(object):
    SAS_PARAMS = {
        SIGNED_PERMISSIONS: "r",
        SIGNED_SERVICE: "t",
        SIGNED_RESOURCE_TYPE: "o",
        SIGNED_EXPIRY: "",
        SIGNED_IP: "",
        SIGNED_VERSION: "2015-04-05"
    }


    def __init__(self, account_name, account_key):
        self.account_name = account_name
        self.account_key = account_key
        expiry_date = datetime.utcnow() + timedelta(days=DAYS_TO_EXPIRY)
        self.SAS_PARAMS[SIGNED_EXPIRY] = expiry_date.strftime('%Y-%m-%dT%H:%MZ')


    def _sign_string(self, string_to_sign, key_is_base64=True):
        if key_is_base64:
            key = decode_base64_to_bytes(self.account_key)
        else:
            if isinstance(key, unicode):
                key = key.encode('utf-8')
        if isinstance(string_to_sign, unicode):
            string_to_sign = string_to_sign.encode('utf-8')
        signed_hmac_sha256 = hmac.HMAC(key, string_to_sign, hashlib.sha256)
        digest = signed_hmac_sha256.digest()
        encoded_digest = encode_base64(digest)
        return encoded_digest


    def _generate_sig(self):
        string_to_sign = \
            self.account_name + '\n' + \
            self.SAS_PARAMS.get(SIGNED_PERMISSIONS, "") + '\n' + \
            self.SAS_PARAMS.get(SIGNED_SERVICE, "") + '\n' + \
            self.SAS_PARAMS.get(SIGNED_RESOURCE_TYPE, "") + '\n' + \
            SIGNED_START + '\n' + \
            self.SAS_PARAMS.get(SIGNED_EXPIRY, "") + '\n' + \
            self.SAS_PARAMS.get(SIGNED_IP, "") + '\n' + \
            SIGNED_PROTOCOL + '\n' + \
            self.SAS_PARAMS.get(SIGNED_VERSION, "") + '\n'
        return self._sign_string(string_to_sign)

    def get_token(self):
        signature = self._generate_sig()
        params_list = ['%s=%s' % (param, value) for (param, value) in self.SAS_PARAMS.items() if value != ""] + \
            ["sig=%s" % quote(signature)]
        token_string = '&'.join(params_list)
        return token_string
