#!/usr/bin/env python3
import re
import sys

def import_txt_1(filename):
    """Text format: text consists of one or more groups divided by newline(s). 
    Each group has a group name followed by one or more addresses on separate lines.
    Group is created as separate host objects and group containing it."""
    groups = []
    with open(filename) as f:
        grp = []
        for line in f:
            if re.match(r"\n+", line):
                if grp:
                    groups.append(grp[:])
                    grp = []
            else:
                grp.append(line)
    cp_hosts = []
    cp_groups = []

    for g in groups:
        group_name = g[0].strip()
        group = {"name": group_name,
                }
        for idx, address in enumerate(g[1:],start=1):
            host = {"name": group_name.strip() + f".{str(idx)}",
                    "ip-address": address.strip()} 
            cp_hosts.append(host)
            group["members."+str(idx)] = host["name"]
        cp_groups.append(group)

    return {"host": cp_hosts,
            "group": cp_groups}

def output_smartconsole(objects, global_values=None):
    output = ""
    for _type in objects:
        for o in objects[_type]:
            s = f"add {_type}"
            for p,v in o.items():
                s += f" {p} {v}"
            for p,v in global_values.items():
                s += f" {p} {v}"
            s += "\n"
            output += s
    return output
                
def import_txt_2(filename):
    """Text format: one netwotk per line, like x.x.x.x/28"""
    cp_networks = []
    with open(filename) as f:
        for line in f:
            if (match := re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d+', line)) is not None:
                cp_network = {'name': match.group(0),
                        "subnet": match.group(0).split('/')[0],
                        "mask-length": match.group(0).split('/')[1]
                        }
                cp_networks.append(cp_network)
    return {"network": cp_networks}

default_import = import_txt_1
default_output = output_smartconsole

class CpObjects:
    def __init__(self, filename, import_plugin=default_import, global_values=None):
        self.cp_objects = import_plugin(filename)
        self.global_values = global_values

    def dump(self, output_plugin=default_output):
        return output_plugin(self.cp_objects, global_values=self.global_values)

if __name__ == "__main__":
    cpo = CpObjects(sys.argv[1], global_values={"ignore-warnings": "true"})
    print(cpo.dump())
