#!/usr/bin/env python
"""Tests for `phpipam_exporter` package."""
# pylint: disable=redefined-outer-name
import json
import os
import sys
from unittest.mock import MagicMock

from click.testing import CliRunner

sys.path.insert(0, 'phpipam_exporter/')
from phpipam_exporter import cli                # noqa: E402


PARAMS = [
    '--host', 'xxx',
    '--token', 'ttt',
    '--subnet', '192.168.1.0/24'
]
BASE_DIR = f'{os.path.dirname(os.path.realpath(__file__))}/'
ADDRESSES_FILE = f'{BASE_DIR}addresses.json'

IPAM = MagicMock()
cli.IPAM = MagicMock(return_value=IPAM)
with open(ADDRESSES_FILE, 'r') as fd:
    IPAM.get_addresses.return_value = json.load(fd)


def get_file(filename: str, param: str):
    def wrapper(fce):
        def call(*args, **kwargs):
            with open(f'{BASE_DIR}results/{filename}', 'r+') as fd:
                kwargs[param] = fd.read()
            return fce(*args, **kwargs)
        return call
    return wrapper


@get_file('hosts.txt', 'hosts')
def test_hosts(hosts):
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main, PARAMS + ['--format', 'hosts'])
    assert result.exit_code == 0
    assert result.output.strip() == hosts.strip()


@get_file('dhcpd.txt', 'dhcpd')
def test_dhcpd(dhcpd):
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main, PARAMS + ['--format', 'dhcpd'])
    assert result.exit_code == 0
    assert result.output.strip() == dhcpd.strip()


@get_file('dnsmasq.txt', 'dnsmasq')
def test_dnsmasq(dnsmasq):
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main, PARAMS + ['--format', 'dnsmasq'])
    assert result.exit_code == 0
    assert result.output.strip() == dnsmasq.strip()
