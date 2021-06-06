"""Main module."""
import logging

from .api import Api

logger = logging.getLogger('IPAM')


class IPAM:

    def __init__(self, uri: str, token: str):
        self.api = Api(uri, headers={'token': token})

    def get_subnet(self, name: str):
        logger.debug(f'Get subnet "{name}".')
        res = self.api.get(f'/subnets/search/{name}/', timeout=10)
        logger.debug(f'Response: {res}')
        if res:
            return res.pop(0)
        return res

    def get_addresses(self, subnets: list):
        _addresses = []
        for subnet in subnets:
            sub = self.get_subnet(subnet)
            if not sub:
                logger.error(f"This subnet '{subnet}' does not exist.")
                continue
            subnet_id = sub.get('id')
            logger.debug(f'Get addresses for subnet "{subnet_id}".')
            _addresses += self.api.get(f'/subnets/{subnet_id}/addresses/',
                                       timeout=20)
        return _addresses
