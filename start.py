from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
AES_KEY = b"12345678abcdefgh"
with open("code.enc","r") as f:
    enc_data_b64 = f.read()
enc_raw = base64.b64decode(enc_data_b64)
cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=AES_KEY)
raw_code = unpad(cipher.decrypt(enc_raw), AES.block_size).decode("utf-8")
exec(raw_code)
