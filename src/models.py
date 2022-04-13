import datetime as dt
import os
import typing as tp

from pydantic import BaseModel

IPFS_DISPLAY_GATEWAY_LINK: str = os.getenv("IPFS_DISPLAY_GATEWAY_LINK", "https://gateway.ipfs.io/ipfs")
BLOCK_EXPLORER_LINK: str = os.getenv("BLOCK_EXPLORER_LINK", "https://robonomics.subscan.io/extrinsic")


class GenericResponse(BaseModel):
    status_code: int
    detail: tp.Optional[str]


class Unit(BaseModel):
    """Unit class corresponds to one uniquely identifiable physical production unit"""

    uuid: str
    internal_id: str
    creation_time: dt.datetime
    passport_short_url: tp.Optional[str]
    passport_ipfs_cid: tp.Optional[str]
    serial_number: tp.Optional[str]
    txn_hash: tp.Optional[str] = None
    ipfs_link: tp.Optional[str] = None
    txn_link: tp.Optional[str] = None

    def __init__(self, **data: tp.Any) -> None:
        super().__init__(**data)

        if self.txn_hash is not None:
            self.txn_link = BLOCK_EXPLORER_LINK + "/" + self.txn_hash

        if self.passport_ipfs_cid is not None:
            self.ipfs_link = IPFS_DISPLAY_GATEWAY_LINK + "/" + self.passport_ipfs_cid


class UnitData(GenericResponse):
    unit_data: Unit


class ProductionStage(BaseModel):
    started_timestamp: str
    ended_timestamp: str
    videos: tp.Optional[tp.List[str]] = None


class CertificateData(BaseModel):
    unit_uuid: str
    unit_name: str
    production_stages: tp.List[ProductionStage]


class CertificateResponse(GenericResponse):
    certificate_data: CertificateData
