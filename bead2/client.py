import sys
import json

with open("cs1.json", "r") as f:
    data = json.load(f)


def get_link(inp_link):
    return [
        link for link in data["links"] if link["points"] == inp_link
        or link["points"] == list(reversed(inp_link))
    ][0]


def check_capacity(path, cap_demand):
    def get_capacity(inp_link):
        return get_link(inp_link)["capacity"]

    return all([
        get_capacity([path[i], path[i + 1]]) >= cap_demand
        for i in range(len(path) - 1)
    ])


def get_path(end_points, ammount):
    paths = [
        path for path in data["possible-circuits"]
        if path[0] == end_points[0] and path[-1] == end_points[-1]
    ]
    possible_paths = [path for path in paths if check_capacity(path, ammount)]

    return min(possible_paths, key=len) if possible_paths else None


def change_link_capacity(link, ammount):
    get_link(link)["capacity"] -= ammount


def change_route_capacity(end_points, ammount):
    path = get_path(end_points, ammount)
    if path is None:
        return False

    for ind in range(len(path) - 1):
        change_link_capacity([path[ind], path[ind + 1]], ammount)

    return True


def main():
    not_created = []
    counter = 1
    for time in range(data["simulation"]["duration"]):
        circuits_to_build = [
            circuit for circuit in data["simulation"]["demands"]
            if circuit["start-time"] == time
        ]

        circuits_to_break = [
            (path["end-points"], -path["demand"])
            for path in data["simulation"]["demands"]
            if path["end-time"] == time and path not in not_created
        ]

        for circuit in circuits_to_break:
            change_route_capacity(*circuit)
            print(
                f"{counter}. igény felszabadítás {circuit[0][0]}<->{circuit[0][1]}"
                f" st:{time}")

            counter += 1

        for circuit in circuits_to_build:
            result = change_route_capacity(circuit["end-points"],
                                           circuit["demand"])

            print(
                f"{counter}. igény foglalás {circuit['end-points'][0]}<->{circuit['end-points'][1]}"
                f" st:{time} - {'sikeres' if result else 'sikertelen'}")

            if not result:
                not_created.append(circuit)
            counter += 1


if __name__ == "__main__":
    main()