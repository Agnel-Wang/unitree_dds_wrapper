from threading import Thread
import rich_click as click
from rich.console import Console
from cyclonedds.tools.cli.utils import (
    TimeDeltaParamType,
    LiveData,
    background_progress_viewer,
    background_printer,
)
from cyclonedds.tools.cli.discovery.main import type_discovery
from rich.syntax import Syntax
from rich.prompt import Prompt
from typing import Any
from cyclonedds import domain, sub, topic
import time
from cyclonedds.internal import InvalidSample

def subscribe(live: LiveData, domain_id: int, topic_name: str, datatype: Any):
    dp = domain.DomainParticipant(domain_id)
    tp = topic.Topic(dp, topic_name, datatype)
    rd = sub.DataReader(dp, tp)

    count = 0
    last_time = time.time()

    while not live.terminate:
        for data in rd.take(N=1):
            if data is None or isinstance(data, InvalidSample):
                continue
            count += 1

        now = time.time()
        if now - last_time >= 1.0:
            live.printables.put(
                f"[{topic_name}] frequency = {count} msgs/s", block=True
            )
            count = 0
            last_time = now

        time.sleep(0.00001)

    live.delivered = True

@click.command(short_help="Compute the frequency of a topic")
@click.argument("topic")
@click.option(
    "-i", "--id", "--domain-id", type=int, default=0, help="DDS Domain to inspect."
)
@click.option(
    "-r",
    "--runtime",
    type=TimeDeltaParamType(),
    default="1s",
    help="Duration of discovery scan.",
)
@click.option(
    "--suppress-progress-bar",
    type=bool,
    is_flag=True,
    help="Suppress the output of the progress bar",
)
def hz(topic, id, runtime, suppress_progress_bar):
    console = Console(color_system=None)
    live = LiveData(console)

    thread = Thread(target=type_discovery, args=(live, id, runtime, topic))
    thread.start()

    console.print()
    background_progress_viewer(runtime, live, suppress_progress_bar)

    thread.join()

    if not live.result:
        console.print(
            "[bold red] :police_car_light: No types could be discovered over XTypes, no dynamic subsciption possible[/]"
        )
        return
    elif len(live.result) > 1:
        console.print(
            "[bold orange] :warning: Multiple type definitions exist, please pick one"
        )

        for i, (_, code, pp) in enumerate(live.result):
            console.print(
                f"Type {i}, As defined in participant(s) [magenta]"
                + ", ".join(f"{p}" for p in pp)
            )
            console.print(Syntax(code, "omg-idl"))
            console.print()

        index = Prompt.ask(
            "Please pick a type:",
            choices=[f"Type {i}" for i in range(len(live.result))],
        )
        index = int(index[len("Type: ") :])

        datatype = live.result[i][0]
    else:
        datatype = live.result[0][0]

    console.print("[bold green] Subscribing, CTRL-C to quit")


    thread = Thread(target=subscribe, args=(live, id, topic, datatype))
    thread.start()

    console.print()
    background_printer(live)
    console.print()

    thread.join()
