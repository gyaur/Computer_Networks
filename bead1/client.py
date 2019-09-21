import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
import sys
import csv
import time


def execute_command(command, site):
    command = f"{command} {site}" if command == "traceroute"\
                                  else f"ping -c 10 {site}"

    process = subprocess.Popen(command.split(),
                               stdout=subprocess.PIPE).communicate()

    return {"target": site, "output": str(process[0])[2:-1]}


def fromat_dict(l, date, platform, list_key):
    return {"date": date, "platform": platform, list_key: l}


def main():
    PLATFORM = "linux"
    DATE = "20190919"
    with open(sys.argv[1], "r") as csv_file:
        data = [v for k, v in csv.reader(csv_file)]

    data = data[:10] + data[-10:]

    with ThreadPoolExecutor(max_workers=20) as pool:
        ping_results = list(
            pool.map(lambda x: execute_command("ping", x), data))

        trace_results = list(
            pool.map(lambda x: execute_command("traceroute", x), data))

    with open("ping.json", "w") as ping_file:
        json.dump(fromat_dict(ping_results, DATE, PLATFORM, "pings"),
                  ping_file)

    with open("traceroute.json", "w") as trace_file:
        json.dump(fromat_dict(trace_results, DATE, PLATFORM, "traces"),
                  trace_file)


if __name__ == "__main__":
    main()
