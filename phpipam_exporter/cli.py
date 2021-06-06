"""Console script for phpipam_exporter."""
import glob
import logging
import os
import subprocess
import sys

from jinja2 import Environment, FileSystemLoader, select_autoescape

import click

from .libs.ipam import IPAM

BASE_DIR = f'{os.path.dirname(os.path.realpath(__file__))}/'


formats = [os.path.basename(it).replace('.j2', '')
           for it in glob.glob(f'{BASE_DIR}templates/*.j2')]


@click.command()
@click.option('--subnet', '-s', help="Subnet. Can be used multiple.",
              required=True, multiple=True, envvar='PHPIPAM_SUBNETS')
@click.option('--format', '-f', type=click.Choice(formats), default=formats[0],
              envvar='PHPIPAM_FORMAT', help="Output format")
@click.option('--host', envvar='PHPIPAM_HOST', required=True,
              help="phpipam API entrypoint. "
                   "(e.g. https://<fqdn>/api/<api_id>/)")
@click.option('--token', envvar='PHPIPAM_TOKEN', required=True,
              help="phpipam API token.")
@click.option('--custom-template', 'custom_template',
              envvar='PHPIPAM_CUSTOM_TEMPLATE',
              help="Custom Jinja template file.", type=click.Path())
@click.option('--output', '-o', 'output_file', envvar='PHPIPAM_OUTPUT',
              help="Output file.", type=click.Path())
@click.option('--on-change-action', 'on_change_action',
              envvar='PHPIPAM_ON_CHANGE_ACTION',
              help="This script is fired when output file is changed.")
def main(subnet, format, host, token, custom_template, output_file,
         on_change_action):
    """
    Export ip addresses from phpipam to many formats.
    """
    try:
        if not format:
            format = 'json'
        template_dir = f"{BASE_DIR}templates"
        template_file = f"{format}.j2"
        if custom_template:
            template_dir = os.path.dirname(custom_template)
            template_file = os.path.basename(custom_template)
        env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape()
        )
        addresses = IPAM(host, token).get_addresses(subnet)
        template = env.get_template(template_file)
        data = template.render(addresses=addresses)
        if output_file:
            overwrite = True
            if on_change_action and os.path.exists(output_file):
                with open(output_file, 'r') as fd_org:
                    original = fd_org.read()
                overwrite = original != data
            if overwrite:
                with open(output_file, 'w+') as fd_out:
                    fd_out.write(data)
                if on_change_action:
                    subprocess.run(on_change_action, check=True, shell=True)
        else:
            click.secho(data, file=sys.stdout)
    except Exception as ex:
        logging.error(ex, exc_info=ex)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
