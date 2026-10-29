import zlib
from typing import IO

# We use the standard-library zlib because its incremental checksum
# objects (zlib.crcobj / zlib.adler32 state) have, in practice, no
# public API that lets us resume them after serialisation. So rather
# than invent one, we drive the built-in crc32() / adler32() directly.
# Both accept an optional initial value and return a uint32; calling
# them in chunks is identical to calling them once over the full
# buffer, which is exactly the property we need for streaming.

# zlib returns the checksum as a signed int on some Python builds and
# an unsigned int on others. Masking with 0xffffffff makes the result
# canonical on every interpreter.
_MASK = 0xFFFFFFFF


def crc32_uint(stream: IO[bytes], chunk_size: int = 65536) -> int:
    """Compute CRC-32 over ``stream`` as an unsigned integer.

    The stream is read in ``chunk_size`` byte pieces so files larger
    than memory are handled. An empty stream yields 0, matching
    ``zlib.crc32(b"")``.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    value = 0
    while True:
        block = stream.read(chunk_size)
        if not block:
            break
        value = zlib.crc32(block, value) & _MASK
    return value


def crc32_hex(stream: IO[bytes], chunk_size: int = 65536) -> str:
    """Compute CRC-32 over ``stream`` as a lowercase hex string of eight digits.

    The width is fixed at eight characters so the output sorts and
    compares cleanly regardless of leading zeros.
    """
    return format(crc32_uint(stream, chunk_size), "08x")


def adler32_uint(stream: IO[bytes], chunk_size: int = 65536) -> int:
    """Compute Adler-32 over ``stream`` as an unsigned integer.

    Reads in fixed-size chunks. An empty stream yields 1, matching
    ``zlib.adler32(b"")``.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    value = 1
    while True:
        block = stream.read(chunk_size)
        if not block:
            break
        value = zlib.adler32(block, value) & _MASK
    return value


def adler32_hex(stream: IO[bytes], chunk_size: int = 65536) -> str:
    """Compute Adler-32 over ``stream`` as a lowercase hex string of eight digits."""
    return format(adler32_uint(stream, chunk_size), "08x")
