from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64, os
AES_KEY = b"12345678abcdefgh"
with open("main.py","r",encoding="utf-8") as f:
    code_text = f.read()
cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=AES_KEY)
encrypted_raw = cipher.encrypt(pad(code_text.encode("utf-8"), AES.block_size))
encrypted_b64 = base64.b64encode(encrypted_raw).decode()
with open("code.enc","w") as f:
    f.write(encrypted_b64)
os.remove("main.py")
