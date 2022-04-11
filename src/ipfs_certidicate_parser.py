import os
import re
import typing as tp

import httpx
import yaml

from models import CertificateData, ProductionStage

IPFS_PARSING_GATEWAY_LINK: str = os.getenv("IPFS_PARSING_GATEWAY_LINK", "https://multiagent.mypinata.cloud/ipfs")


def _extract_cid(ipfs_uri: str) -> str:
    cid_pattern = r"Qm[A-Za-z0-9]{44}"
    cid = re.search(cid_pattern, ipfs_uri)

    if cid is None:
        raise ValueError(f"String '{ipfs_uri}' does not contain a valid IPFS CID")

    return cid[0]


async def _get_file_from_ipfs(ipfs_cid: str) -> bytes:
    """get file with the provided CID from IPFS and return it's contents"""
    ipfs_cid = _extract_cid(ipfs_cid)

    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.get(IPFS_PARSING_GATEWAY_LINK + "/" + ipfs_cid)
        assert response.status_code == 200
        return response.content


@tp.no_type_check
def _parse_certificate_file(file: bytes) -> tp.Dict[str, tp.Any]:
    return yaml.safe_load(file)


async def parse_certificate(cid: str) -> CertificateData:
    data = await _get_file_from_ipfs(cid)
    certificate_dict = _parse_certificate_file(data)
    return CertificateData(
        unit_uuid=certificate_dict.get("Уникальный номер паспорта изделия", ""),
        unit_name=certificate_dict.get("Модель изделия", ""),
        production_stages=[
            ProductionStage(
                started_timestamp=stage.get("Время начала", ""),
                ended_timestamp=stage.get("Время окончания", ""),
                videos=stage.get("Видеозаписи процесса сборки в IPFS"),
            )
            for stage in certificate_dict.get("Этапы производства", [])
        ]
        or None,
    )
