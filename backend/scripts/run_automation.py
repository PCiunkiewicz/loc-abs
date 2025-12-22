"""Run automation script."""

import copy
import itertools
import json

from api.simulation import models
from api.simulation.serializers import NestedRunSerializer
from simulation.launcher import SimLauncher
from utilities import paths
from utilities.scripting import ORMScript

VAX_TYPES = ('MRNA', 'ASTRA')
VAX_DOSES = (0, 1, 2)
MASK_TYPES = ('N95', 'NONE', 'CLOTH', 'SURGICAL')


class Script(ORMScript):
    """Automation script to run multiple scenarios with different protection strategies."""

    def run(self) -> None:
        """Run the script."""
        scenario = models.Scenario.objects.get(id=34)
        agent_config = models.AgentConfig.objects.get(id=1)

        combinations = itertools.product(MASK_TYPES, VAX_TYPES, VAX_DOSES)

        for mask, vax, dose in combinations:
            if vax == 'ASTRA' and dose == 0:
                continue  # Skip duplicate 0-dose runs

            agents = copy.deepcopy(agent_config)
            agents.default['info']['mask_type'] = mask
            agents.default['info']['vax_type'] = vax
            agents.default['info']['vax_doses'] = dose

            run = models.Run(
                name=f'{scenario.name}_mask={mask}_vax={vax}_dose={dose}',
                scenario=scenario,
                agents=agents,
                runs=1024,
            )

            run.save()
            run.save_dir = paths.OUTPUTS.rel / f'{run.id:03}-{run.name}'
            run.logfile = paths.LOGS.rel / f'{run.id:03}-{run.name}.log'
            run.config = paths.CFG.rel / f'{run.id:03}-{run.name}.json'
            run.save()

            run.config.write_text(json.dumps(NestedRunSerializer(run).data, indent=2))

            launcher = SimLauncher(run)
            launcher.start(await_results=False)
