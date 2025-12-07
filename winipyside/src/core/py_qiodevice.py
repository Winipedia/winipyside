"""PySide6 QIODevice wrapper."""

import os
from collections.abc import Generator
from functools import partial
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from PySide6.QtCore import QFile, QIODevice


class PyQIODevice(QIODevice):
    """Pythonic wrapper for PySide6 QIODevice with transparent delegation.

    This class provides a Python-friendly interface to PySide6's QIODevice by wrapping
    an existing QIODevice instance and delegating all I/O operations to it. This pattern
    allows for composition-based enhancement of QIODevice functionality
    while maintaining full API compatibility.

    The wrapper implements all standard QIODevice methods,
    making it suitable as a drop-in
    replacement for QIODevice in contexts requiring Pythonic behavior or additional
    processing layers (e.g., encryption/decryption in subclasses).
    """

    def __init__(self, q_device: QIODevice, *args: Any, **kwargs: Any) -> None:
        """Initialize the PyQIODevice wrapper.

        Args:
            q_device: The QIODevice instance to wrap and delegate operations to.
            *args:
                Additional positional arguments passed to parent QIODevice constructor.
            **kwargs:
                Additional keyword arguments passed to parent QIODevice constructor.
        """
        super().__init__(*args, **kwargs)
        self.q_device = q_device

    def atEnd(self) -> bool:  # noqa: N802
        """Check if the device is at the end of data.

        Returns:
            True if the device is at the end, False otherwise.
        """
        return self.q_device.atEnd()

    def bytesAvailable(self) -> int:  # noqa: N802
        """Get the number of bytes available for reading.

        Returns:
            The number of bytes available for reading.
        """
        return self.q_device.bytesAvailable()

    def bytesToWrite(self) -> int:  # noqa: N802
        """Get the number of bytes waiting to be written.

        Returns:
            The number of bytes waiting to be written.
        """
        return self.q_device.bytesToWrite()

    def canReadLine(self) -> bool:  # noqa: N802
        """Check if a complete line can be read from the device.

        Returns:
            True if a complete line can be read, False otherwise.
        """
        return self.q_device.canReadLine()

    def close(self) -> None:
        """Close the device and release resources.

        Closes the underlying QIODevice and calls the parent close method.
        """
        self.q_device.close()
        return super().close()

    def isSequential(self) -> bool:  # noqa: N802
        """Check if the device is sequential.

        Returns:
            True if the device is sequential, False if it supports random access.
        """
        return self.q_device.isSequential()

    def open(self, mode: QIODevice.OpenModeFlag) -> bool:
        """Open the device with the specified mode.

        Args:
            mode: The open mode flag specifying how to open the device.

        Returns:
            True if the device was opened successfully, False otherwise.
        """
        self.q_device.open(mode)
        return super().open(mode)

    def pos(self) -> int:
        """Get the current position in the device.

        Returns:
            The current position in the device.
        """
        return self.q_device.pos()

    def readData(self, maxlen: int) -> bytes:  # noqa: N802
        """Read data from the device.

        Args:
            maxlen: The maximum number of bytes to read.

        Returns:
            The data read from the device as bytes.
        """
        return bytes(self.q_device.read(maxlen).data())

    def readLineData(self, maxlen: int) -> object:  # noqa: N802
        """Read a line from the device.

        Args:
            maxlen: The maximum number of bytes to read.

        Returns:
            The line data read from the device.
        """
        return self.q_device.readLine(maxlen)

    def reset(self) -> bool:
        """Reset the device to its initial state.

        Returns:
            True if the device was reset successfully, False otherwise.
        """
        return self.q_device.reset()

    def seek(self, pos: int) -> bool:
        """Seek to a specific position in the device.

        Args:
            pos: The position to seek to.

        Returns:
            True if the seek operation was successful, False otherwise.
        """
        return self.q_device.seek(pos)

    def size(self) -> int:
        """Get the size of the device.

        Returns:
            The size of the device in bytes.
        """
        return self.q_device.size()

    def skipData(self, maxSize: int) -> int:  # noqa: N802, N803
        """Skip data in the device.

        Args:
            maxSize: The maximum number of bytes to skip.

        Returns:
            The actual number of bytes skipped.
        """
        return self.q_device.skip(maxSize)

    def waitForBytesWritten(self, msecs: int) -> bool:  # noqa: N802
        """Wait for bytes to be written to the device.

        Args:
            msecs: The maximum time to wait in milliseconds.

        Returns:
            True if bytes were written within the timeout, False otherwise.
        """
        return self.q_device.waitForBytesWritten(msecs)

    def waitForReadyRead(self, msecs: int) -> bool:  # noqa: N802
        """Wait for the device to be ready for reading.

        Args:
            msecs: The maximum time to wait in milliseconds.

        Returns:
            True if the device became ready within the timeout, False otherwise.
        """
        return self.q_device.waitForReadyRead(msecs)

    def writeData(self, data: bytes | bytearray | memoryview, len: int) -> int:  # noqa: A002, ARG002, N802
        """Write data to the device.

        Args:
            data: The data to write to the device.
            len: The length parameter (unused in this implementation).

        Returns:
            The number of bytes actually written.
        """
        return self.q_device.write(data)


class PyQFile(PyQIODevice):
    """Pythonic wrapper for PySide6 QFile with file path support.

    A specialized PyQIODevice wrapper that handles file path initialization and
    provides convenient file I/O operations. This class extends PyQIODevice with
    automatic QFile instantiation from file paths, simplifying file-based I/O
    operations throughout the application.
    """

    def __init__(self, path: Path, *args: Any, **kwargs: Any) -> None:
        """Initialize the PyQFile with a file path.

        Args:
            path: The file path to open.
            *args: Additional positional arguments passed to parent constructor.
            **kwargs: Additional keyword arguments passed to parent constructor.
        """
        super().__init__(QFile(path), *args, **kwargs)
        self.q_device: QFile


class EncryptedPyQFile(PyQFile):
    """Transparent AES-GCM encrypted file wrapper for secure media access.

    This class provides transparent encryption/decryption for file operations using
    AES-GCM (Galois/Counter Mode), an authenticated encryption cipher. Data is encrypted
    in fixed-size chunks (64KB plaintext + overhead) to support efficient streaming and
    random-access playback without decrypting entire files into memory.

    Why chunked encryption is used:
    This approach enables seeking through encrypted files
    and playing encrypted videos without temporary files,
    by mapping between encrypted and
    decrypted positions and decrypting only necessary chunks on demand.

    Attributes:
        NONCE_SIZE: Size of random nonce per chunk (12 bytes).
        CIPHER_SIZE: Size of plaintext per chunk (64 KB).
        TAG_SIZE: Size of authentication tag per chunk (16 bytes).
        CHUNK_SIZE: Total encrypted chunk size = CIPHER_SIZE + NONCE_SIZE + TAG_SIZE.
        CHUNK_OVERHEAD: Total per-chunk overhead = NONCE_SIZE + TAG_SIZE (28 bytes).
    """

    NONCE_SIZE = 12
    CIPHER_SIZE = 64 * 1024
    TAG_SIZE = 16
    CHUNK_SIZE = CIPHER_SIZE + NONCE_SIZE + TAG_SIZE
    CHUNK_OVERHEAD = NONCE_SIZE + TAG_SIZE

    def __init__(self, path: Path, aes_gcm: AESGCM, *args: Any, **kwargs: Any) -> None:
        """Initialize the encrypted file wrapper.

        Args:
            path: The file path to open.
            aes_gcm: The AES-GCM cipher instance for encryption/decryption.
            *args: Additional positional arguments passed to parent constructor.
            **kwargs: Additional keyword arguments passed to parent constructor.
        """
        super().__init__(path, *args, **kwargs)
        self.q_device: QFile
        self.aes_gcm = aes_gcm
        self.dec_size = self.size()

    def readData(self, maxlen: int) -> bytes:  # noqa: N802
        """Read and decrypt data from the encrypted file.

        Implements transparent decryption by reading encrypted chunks from the file
        and decrypting them. Handles position mapping between encrypted and decrypted
        data, enabling random access and seeking within encrypted content.

        This method is called internally by the QIODevice read() method and handles
        the complexity of chunk boundaries and position tracking.

        Args:
            maxlen: The maximum number of decrypted bytes to read from current position.

        Returns:
            The decrypted data as bytes (may be less than maxlen if at end of file).
        """
        # where we are in the encrypted data
        dec_pos = self.pos()
        # where we are in the decrypted data
        enc_pos = self.get_encrypted_pos(dec_pos)

        # get the chunk start and end
        chunk_start = self.get_chunk_start(enc_pos)
        chunk_end = self.get_chunk_end(enc_pos, maxlen)
        new_maxlen = chunk_end - chunk_start

        # read the chunk
        self.seek(chunk_start)
        enc_data = super().readData(new_maxlen)
        # decrypt the chunk
        dec_data = self.decrypt_data(enc_data)

        # get the start and end of the requested data in the decrypted data
        dec_chunk_start = self.get_decrypted_pos(chunk_start + self.NONCE_SIZE)

        req_data_start = dec_pos - dec_chunk_start
        req_data_end = req_data_start + maxlen

        dec_pos += maxlen
        self.seek(dec_pos)

        return dec_data[req_data_start:req_data_end]

    def writeData(self, data: bytes | bytearray | memoryview, len: int) -> int:  # noqa: A002, ARG002, N802
        """Encrypt and write data to the file.

        Encrypts the provided plaintext data using AES-GCM and writes the encrypted
        chunks to the underlying file device. Each chunk includes a random nonce and
        authentication tag for authenticated encryption.

        Args:
            data: The plaintext data to encrypt and write.
            len: The length parameter (unused in this implementation,
                actual data length is used).

        Returns:
            The number of plaintext bytes that were encrypted and written.
        """
        encrypted_data = self.encrypt_data(bytes(data))
        encrypted_len = encrypted_data.__len__()
        return super().writeData(encrypted_data, encrypted_len)

    def size(self) -> int:
        """Get the decrypted file size.

        Calculates and caches the decrypted file size based on the encrypted file size
        and chunk structure. This is used internally by the media player to determine
        file bounds without decrypting the entire file.

        Returns:
            The total plaintext size of the file in bytes.
        """
        self.enc_size = super().size()
        self.num_chunks = self.enc_size // self.CHUNK_SIZE + 1
        self.dec_size = self.num_chunks * self.CIPHER_SIZE
        return self.dec_size

    def get_decrypted_pos(self, enc_pos: int) -> int:
        """Convert encrypted file position to decrypted (plaintext) position.

        Maps positions from the encrypted file layout to the corresponding position
        in the plaintext stream. Accounts for nonces and tags distributed across chunks.

        This is essential for seeking operations - when user seeks to position X in the
        plaintext, we need to find the corresponding position in the encrypted file.

        Args:
            enc_pos: The byte position in the encrypted file.

        Returns:
            The corresponding byte position in the decrypted plaintext.
        """
        if enc_pos >= self.enc_size:
            return self.dec_size

        num_chunks_before = enc_pos // self.CHUNK_SIZE
        last_enc_chunk_start = num_chunks_before * self.CHUNK_SIZE
        last_dec_chunk_start = num_chunks_before * self.CIPHER_SIZE

        enc_bytes_to_move = enc_pos - last_enc_chunk_start

        return last_dec_chunk_start + enc_bytes_to_move - self.NONCE_SIZE

    def get_encrypted_pos(self, dec_pos: int) -> int:
        """Convert decrypted (plaintext) position to encrypted file position.

        Maps positions from the plaintext stream to the corresponding position
        in the encrypted file layout.
        Accounts for nonces and tags distributed across chunks.

        This is the inverse of get_decrypted_pos() and is used when seeking - we convert
        the desired plaintext position to find where to read in the encrypted file.

        Args:
            dec_pos: The byte position in the decrypted plaintext stream.

        Returns:
            The corresponding byte position in the encrypted file.
        """
        if dec_pos >= self.dec_size:
            return self.enc_size
        num_chunks_before = dec_pos // self.CIPHER_SIZE
        last_dec_chunk_start = num_chunks_before * self.CIPHER_SIZE
        last_enc_chunk_start = num_chunks_before * self.CHUNK_SIZE

        dec_bytes_to_move = dec_pos - last_dec_chunk_start

        return last_enc_chunk_start + self.NONCE_SIZE + dec_bytes_to_move

    def get_chunk_start(self, pos: int) -> int:
        """Get the start byte position of the chunk containing the given position.

        Calculates which chunk boundary contains the position and returns the
        byte offset where that chunk begins in the encrypted file.

        Args:
            pos: The byte position within a chunk (encrypted file coordinates).

        Returns:
            The byte offset of the start of the chunk containing the position.
        """
        return pos // self.CHUNK_SIZE * self.CHUNK_SIZE

    def get_chunk_end(self, pos: int, maxlen: int) -> int:
        """Get the end byte position of chunk range for given position and length.

        Determines how many chunks are needed to read maxlen bytes starting from pos,
        and returns the byte offset of the end of the last required chunk.

        Args:
            pos: The starting byte position in the encrypted file.
            maxlen: The number of bytes to potentially read.

        Returns:
            The byte offset of the end of the last chunk needed for the read.
        """
        return (pos + maxlen) // self.CHUNK_SIZE * self.CHUNK_SIZE + self.CHUNK_SIZE

    @classmethod
    def chunk_generator(
        cls, data: bytes, *, is_encrypted: bool
    ) -> Generator[bytes, None, None]:
        """Generate fixed-size chunks from data for streaming processing.

        Yields chunks of the appropriate size based on whether data is encrypted
        or plaintext. Used internally for batch encryption/decryption operations.

        Args:
            data: The complete data to split into chunks.
            is_encrypted: If True, uses CHUNK_SIZE (encrypted). If False, uses
                CIPHER_SIZE (plaintext).

        Yields:
            Byte chunks of the appropriate size (last chunk may be smaller).
        """
        size = cls.CHUNK_SIZE if is_encrypted else cls.CIPHER_SIZE
        for i in range(0, len(data), size):
            yield data[i : i + size]

    def encrypt_data(self, data: bytes) -> bytes:
        """Encrypt plaintext data using this instance's AES-GCM cipher.

        Delegates to the static encryption method with this instance's cipher.

        Args:
            data: The plaintext data to encrypt.

        Returns:
            The encrypted data with nonce
            and authentication tag prepended to each chunk.
        """
        return self.encrypt_data_static(data, self.aes_gcm)

    @classmethod
    def encrypt_data_static(cls, data: bytes, aes_gcm: AESGCM) -> bytes:
        """Encrypt plaintext data using AES-GCM in streaming chunks.

        Processes data in fixed-size plaintext chunks, encrypting each independently.
        Each chunk receives its own random nonce and authentication tag, enabling
        random-access decryption (decrypting any chunk without decrypting others).

        Args:
            data: The plaintext data to encrypt (any size).
            aes_gcm: The AES-GCM cipher instance for encryption.

        Returns:
            The encrypted data with nonces
            and authentication tags prepended to each chunk.
        """
        decrypted_chunks = cls.chunk_generator(data, is_encrypted=False)
        encrypted_chunks = map(
            partial(cls.encrypt_chunk_static, aes_gcm=aes_gcm), decrypted_chunks
        )
        return b"".join(encrypted_chunks)

    @classmethod
    def encrypt_chunk_static(cls, data: bytes, aes_gcm: AESGCM) -> bytes:
        """Encrypt a single plaintext chunk with authenticated encryption.

        Generates a random 12-byte nonce and encrypts the chunk with Additional
        Authenticated Data (AAD) to prevent tampering. The nonce is prepended to
        the ciphertext for use during decryption.

        Args:
            data: The plaintext chunk to encrypt (up to CIPHER_SIZE bytes).
            aes_gcm: The AES-GCM cipher instance for encryption.

        Returns:
            Encrypted chunk formatted as: nonce || ciphertext || authentication_tag.
        """
        nonce = os.urandom(12)
        aad = cls.__name__.encode()
        return nonce + aes_gcm.encrypt(nonce, data, aad)

    def decrypt_data(self, data: bytes) -> bytes:
        """Decrypt encrypted data using this instance's AES-GCM cipher.

        Delegates to the static decryption method with this instance's cipher.

        Args:
            data: The encrypted data with nonces and tags intact.

        Returns:
            The decrypted plaintext data.

        Raises:
            cryptography.exceptions.InvalidTag: If authentication tag verification fails
                (indicates tampering or corruption).
        """
        return self.decrypt_data_static(data, self.aes_gcm)

    @classmethod
    def decrypt_data_static(cls, data: bytes, aes_gcm: AESGCM) -> bytes:
        """Decrypt encrypted data using AES-GCM in streaming chunks.

        Processes encrypted data in chunk-sized blocks, decrypting each independently
        with authenticated verification. Each chunk contains its own nonce, making this
        suitable for random-access scenarios where only specific chunks need decryption.

        Args:
            data: The encrypted data with nonces and tags
                (any size multiple of CHUNK_SIZE).
            aes_gcm: The AES-GCM cipher instance for decryption.

        Returns:
            The decrypted plaintext data.

        Raises:
            cryptography.exceptions.InvalidTag: If any chunk fails authentication
                (indicates tampering, corruption, or wrong key).
        """
        encrypted_chunks = cls.chunk_generator(data, is_encrypted=True)
        decrypted_chunks = map(
            partial(cls.decrypt_chunk_static, aes_gcm=aes_gcm), encrypted_chunks
        )
        return b"".join(decrypted_chunks)

    @classmethod
    def decrypt_chunk_static(cls, data: bytes, aes_gcm: AESGCM) -> bytes:
        """Decrypt a single chunk with authenticated verification.

        Extracts the nonce from the chunk prefix, verifies the authentication tag,
        and decrypts the ciphertext. The AAD must match what was used during encryption.

        Args:
            data: The encrypted chunk formatted as:
                nonce || ciphertext || authentication_tag.
            aes_gcm: The AES-GCM cipher instance for decryption.

        Returns:
            The decrypted plaintext chunk.

        Raises:
            cryptography.exceptions.InvalidTag: If the authentication tag is invalid,
                indicating the chunk was tampered with, corrupted, or encrypted with
                a different key.
        """
        nonce = data[: cls.NONCE_SIZE]
        cipher_and_tag = data[cls.NONCE_SIZE :]
        aad = cls.__name__.encode()
        return aes_gcm.decrypt(nonce, cipher_and_tag, aad)
