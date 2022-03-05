# -*- coding:utf-8 -*-
import base64
import unittest
from cowkit.qcow_header import qcow_parse_header


class TestQCowHeader(unittest.TestCase):

    def setUp(self) -> None:
        # First 255 bytes from `cirros-0.5.2-x86_64-disk.img`, Base64 encoded.
        self.encoded_header = b'UUZJ+wAAAAMAAAAAAAAAAAAAAAAAAAAQAAAAAAcAAAAAAAAAAAAAAQAAAAAAAwAAAAAAAAABAAAAAAAB' \
                              b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAGhoA/hXAAABIAAAZGlydHkg' \
                              b'Yml0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABY29ycnVwdCBiaXQAAAAAAAAA' \
                              b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACZXh0ZXJuYWwgZGF0YSBmaWxlAAAAAAAAAAAAAAAA' \
                              b'AAAAAAAAAAAAAAAAAAAA'
        self.header = base64.b64decode(self.encoded_header)
        self.size = 117440512

    def test_parse(self):
        parsed = qcow_parse_header(self.header)
        self.assertEqual(self.size, parsed.size)
