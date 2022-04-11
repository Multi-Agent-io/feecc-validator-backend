from enum import Enum


class KeyTypes(str, Enum):
    """Available key types for unit identification"""

    uuid = "uuid"
    internal_id = "internal_id"
    passport_ipfs_cid = "ipfs_cid"
    passport_short_url = "short_url"
    txn_hash = "txn_hash"
