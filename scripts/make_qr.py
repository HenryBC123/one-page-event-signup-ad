"""產生海報用的 QR code（SVG，深色碼＋米白底，配海報暗色系）。

用法：python3 make_qr.py <網址> <輸出.svg>
需要 segno：沒裝就 pip3 install --target <暫存資料夾>/py segno，再用 PYTHONPATH=<暫存資料夾>/py 執行。
"""
import sys

import segno

qr = segno.make(sys.argv[1], error="m")
qr.save(sys.argv[2], scale=10, border=2, dark="#1d1a17", light="#faf7f2")
print("version", qr.version, "→", sys.argv[2])
