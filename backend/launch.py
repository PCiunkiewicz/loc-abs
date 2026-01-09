"""Simulation manual run entrypoint."""

import argparse

from simulation.launcher import SimLauncher
from utilities.cli import LauncherCLI, ScriptCLI
from utilities.logs import configure_logger
from utilities.paths import CFG
from utilities.profiling import Profiler

MANUAL_CONFIG = {
    'config': CFG / 'bsf.json',
    'runs': 32,
}

if __name__ == '__main__':
    configure_logger('TRACE')
    parser = argparse.ArgumentParser(prog='Loc-ABS', description='Main simulation launcher.')
    parser.add_argument('--script', action='store_true', help='Run in "script mode".')
    parser.add_argument('--profile', action='store_true', help='Enable profiling.')
    parser.add_argument('--manual', action='store_true', help='Use manual launch config.')
    args = parser.parse_args()

    if args.script:
        cli = ScriptCLI()
        script = cli.prompt()
        if cli.confirm():
            script.run()
    else:
        launch_config = MANUAL_CONFIG if args.manual else LauncherCLI().prompt()
        launcher = SimLauncher.from_config(**launch_config)

        if args.profile:
            profiler = Profiler(launcher.run.logfile, module=['/backend/'])
            profiler.profile(launcher.start)
        else:
            launcher.start()
