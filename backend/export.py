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
    exporter = ExportHandler(run)

    exporter.export(**export_config)

# from pathlib import Path

# from tools.animation import SimAnimation
# from tools.snapshot import SimSnapshot
# from tools.stats import ExcessRiskVsTime
# from utilities.logging import configure_logger
# from utilities.paths import EXPORTS, MAPFILES, OUTPUTS


# def animation(results: Path, mapfile: Path, outfile: Path = EXPORTS / 'animation.gif', html: bool = False) -> None:
#     """Export simulation animation as gif."""
#     SimAnimation(results, mapfile).export(outfile, html)


# def snapshot(results: Path, mapfile: Path, frame: int = 0, outfile: Path = EXPORTS / 'snapshot.png') -> None:
#     """Export simulation frame as image."""
#     SimSnapshot(results, mapfile).export(frame, outfile)


# def excess_risk(config: Path, results: Path, outfile: Path = EXPORTS / 'excess_risk.png') -> None:
#     """Export simulation stats as image."""
#     ExcessRiskVsTime(config, results).export(outfile)


# if __name__ == '__main__':
#     configure_logger('TRACE')

# SimAnimation(
#     OUTPUTS / 'bsf2_test.hdf5',
#     MAPFILES / 'bow_view_manor',
# ).export(EXPORTS / 'bsf2_test2.gif', html=False)
