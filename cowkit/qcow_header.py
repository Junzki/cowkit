# -*- coding:utf-8 -*-
"""

https://people.gnome.org/~markmc/qcow-image-format.html
"""
import dataclasses
import struct

from typing import List

QCOW_HEADER_SIZE = 72
QCOW_MAGIC = b'QFI\xfb'

QCOW_HEADER_GROUP_META = 8
QCOW_HEADER_GROUP_BACKING_FILE = 12
QCOW_HEADER_GROUP_SIZE = 16
QCOW_HEADER_GROUP_L1 = 12
QCOW_HEADER_GROUP_REFCOUNT = 12
QCOW_HEADER_GROUP_SNAPSHOT = 12

QCOW_HEADER_SEG = (
    QCOW_HEADER_GROUP_META,
    QCOW_HEADER_GROUP_BACKING_FILE,
    QCOW_HEADER_GROUP_SIZE,
    QCOW_HEADER_GROUP_L1,
    QCOW_HEADER_GROUP_REFCOUNT,
    QCOW_HEADER_GROUP_SNAPSHOT
)


@dataclasses.dataclass
class QCowHeader:
    magic: bytes = QCOW_MAGIC
    version: int = 1

    backing_file_offset: int = 0
    backing_file_size: int = 0

    cluster_bits: int = 0
    size: int = 0
    crypt_method: int = 0

    l1_size: int = 0
    l1_table_offset: int = 0

    refcount_table_offset: int = 0
    refcount_table_clusters: int = 0

    nb_snapshots: int = 0
    snapshots_offset: int = 0


def qcow_guess_type(header: bytes) -> bool:
    magic = header[:len(QCOW_MAGIC)]
    return QCOW_MAGIC == magic


def qcow_split_header(header: bytes) -> List[bytes]:
    slices = list()
    ptr = 0

    for seg in QCOW_HEADER_SEG:
        next_ = ptr + seg
        s = header[ptr:next_]
        ptr = next_
        slices.append(s)

    return slices


def qcow_parse_header(header: bytes) -> QCowHeader:
    if not qcow_guess_type(header):
        raise ValueError("Not a QCOW Image")

    slices = qcow_split_header(header)
    meta_, backing_, size_, l1_, refcount_, snapshot_ = slices

    _, version_ = struct.unpack('>II', meta_)
    backing_file_offset, backing_file_size = struct.unpack('>QI', backing_)
    cluster_bits, size, crypt_method = struct.unpack('>IQI', size_)
    l1_size, l1_table_offset = struct.unpack('>IQ', l1_)
    refcount_table_offset, refcount_table_clusters = struct.unpack('>QI', refcount_)
    nb_snapshots, snapshots_offset = struct.unpack('>IQ', snapshot_)

    return QCowHeader(QCOW_MAGIC, version_,
                      backing_file_offset, backing_file_size,
                      cluster_bits, size, crypt_method,
                      l1_size, l1_table_offset,
                      refcount_table_offset, refcount_table_clusters,
                      nb_snapshots, snapshots_offset)
