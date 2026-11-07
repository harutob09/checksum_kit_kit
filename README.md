# checksum_kit_kit

CRC-32 and Adler-32 over a stream without loading the whole file into memory.

## Usage

```python
import io
from checksum_kit_kit import crc32_hex, crc32_uint, adler32_hex, adler32_uint

print(crc32_hex(io.BytesIO(b"123456789")))   # 'cbf43926'
print(crc32_uint(io.BytesIO(b"123456789")))   # 3421780262
print(adler32_hex(io.BytesIO(b"123456789"))) # '091e01de'
print(adler32_uint(io.BytesIO(b"123456789")))# 152642270
```

## Why

The standard library's `zlib.crc32` and `zlib.adler32` already accept
an initial value, so streaming a file in chunks is cheap and correct —
but you have to remember to chain the previous value into each call and
to mask the result with `0xffffffff` because Python's `zlib` may return
a signed integer on some interpreters. `checksum_kit_kit` does that for
you and hands back a clean unsigned int or a fixed-width eight-character
hex string.

The trade-off is that nothing here resumes a checksum after
serialisation or exposes incremental state objects: you get the final
digest in one pass. That covers the common case — hashing a file or
socket from start to finish — and keeps the surface tiny.

## Edge you will hit

`crc32_uint` of an empty stream is `0`, and `adler32_uint` of an empty
stream is `1`. These match `zlib.crc32(b"")` and `zlib.adler32(b"")`
respectively. If you store digests and compare against values produced
by tools that emit an empty-file checksum of `"00000000"`, note that
Adler-32's canonical empty value is `0x00000001`, not zero.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

