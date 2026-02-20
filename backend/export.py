"""Generate export snapshots, statistics, and animations."""

import argparse

from tools.handler import ExportHandler
from utilities.cli import ExporterCLI
from utilities.logs import configure_logger

if __name__ == '__main__':
    configure_logger('TRACE')
    parser = argparse.ArgumentParser(prog='Loc-ABS', description='Main simulation launcher.')
    parser.add_argument('--profile', action='store_true', help='Enable profiling.')
    parser.add_argument('--manual', action='store_true', help='Use manual launch config.')
    args = parser.parse_args()

    export_config = {} if args.manual else ExporterCLI().prompt()
    run = export_config.pop('run')
    run_file = export_config.pop('run_file')

    handler = ExportHandler(run, run_file)
    handler.export(**export_config)
