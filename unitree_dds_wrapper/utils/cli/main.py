import rich_click as click

from cyclonedds.tools.cli.settings import CONTEXT_SETTINGS
from cyclonedds.tools.cli.ls import ls
from cyclonedds.tools.cli.ps import ps
from cyclonedds.tools.cli.typeof import typeof
from cyclonedds.tools.cli.sub import subscribe
from cyclonedds.tools.cli.ddsperf import performance

from unitree_dds_wrapper.utils.cli.hz import hz

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    # Initialize the CLI group
    pass


cli.add_command(ls)
cli.add_command(ps)
cli.add_command(typeof)
cli.add_command(subscribe)
cli.add_command(performance)
cli.add_command(hz)

if __name__ == "__main__":
    cli()
