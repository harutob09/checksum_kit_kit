import io
import unittest
import zlib

from checksum_kit_kit.core import (
    crc32_hex,
    crc32_uint,
    adler32_hex,
    adler32_uint,
)


class TestCRC32(unittest.TestCase):
    def test_known_ascii(self):
        self.assertEqual(crc32_uint(io.BytesIO(b"123456789")), 0xCBF43926)

    def test_hex_format(self):
        self.assertEqual(crc32_hex(io.BytesIO(b"123456789")), "cbf43926")

    def test_empty(self):
        self.assertEqual(crc32_uint(io.BytesIO(b"")), 0)
        self.assertEqual(crc32_hex(io.BytesIO(b"")), "00000000")

    def test_large_matches_single_call(self):
        data = b"x" * 1_000_000
        expected = zlib.crc32(data) & 0xFFFFFFFF
        self.assertEqual(crc32_uint(io.BytesIO(data)), expected)

    def test_chunked_matches_unchunked(self):
        data = b"The quick brown fox jumps over the lazy dog. " * 1000
        big = crc32_uint(io.BytesIO(data), chunk_size=64)
        one = crc32_uint(io.BytesIO(data), chunk_size=1 << 24)
        self.assertEqual(big, one)

    def test_bad_chunk_size(self):
        with self.assertRaises(ValueError):
            crc32_uint(io.BytesIO(b"data"), chunk_size=0)
        with self.assertRaises(ValueError):
            crc32_uint(io.BytesIO(b"data"), chunk_size=-1)


class TestAdler32(unittest.TestCase):
    def test_known_ascii(self):
        self.assertEqual(adler32_uint(io.BytesIO(b"123456789")), 0x091E01DE)

    def test_hex_format(self):
        self.assertEqual(adler32_hex(io.BytesIO(b"123456789")), "091e01de")

    def test_empty(self):
        self.assertEqual(adler32_uint(io.BytesIO(b"")), 1)
        self.assertEqual(adler32_hex(io.BytesIO(b"")), "00000001")

    def test_large_matches_single_call(self):
        data = b"y" * 2_000_000
        expected = zlib.adler32(data) & 0xFFFFFFFF
        self.assertEqual(adler32_uint(io.BytesIO(data)), expected)

    def test_chunked_matches_unchunked(self):
        data = b"Pack my box with five dozen liquor jugs. " * 2000
        small = adler32_uint(io.BytesIO(data), chunk_size=37)
        large = adler32_uint(io.BytesIO(data), chunk_size=1 << 20)
        self.assertEqual(small, large)

    def test_bad_chunk_size(self):
        with self.assertRaises(ValueError):
            adler32_uint(io.BytesIO(b"data"), chunk_size=0)


if __name__ == "__main__":
    unittest.main()
