# This is a pretty silly script, but I find myself constantly wanting to just
# run multiple commands on multiple machines - sometimes in parallel, sometimes
# one after another. I've had Ansible recommended to me before, but Ansible does
# a ton of stuff that I don't need. My requirements are simple. The program
# should simply run a bunch of shell commands (parallel or sequential) on
# different hosts. This can be accomplished via a YAML file and some simple
# scripting.

# Prerequisites:
# Root SSH keys installed between the node this is running on and the hosts.
import argparse
import multiprocessing as mp
import os
import subprocess
import yaml

def ssh_cmd(node_name, commands, lock):
    joined_cmds = ";".join(commands)
    args = ['sudo', 'ssh', node_name, joined_cmds]
    
    subprocess.run(args, capture_output=True, text=True, check=True)
    
    lock.acquire()
    try:
        print(node_name, ": SUCCESS")
    finally:
        lock.release()


def exec_block(block):

    procs = []
    lock = mp.Lock()

    for host in block["hosts"]:
        proc = mp.Process(target=ssh_cmd, args=(host, block["commands"], lock))
        procs.append(proc)

    # Start all processes:
    for proc in procs:
        proc.start()
    
    # Wait for processes to finish:
    for proc in procs:
        proc.join()


def main():
    # Get path to config file from args:
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file", help="Path to config file.")
    args = parser.parse_args()

    # Load config file:
    with open(args.config_file) as conf_file:
        conf = yaml.full_load(conf_file)

    for i, block in enumerate(conf["blocks"]):
        print(f"[BLOCK {i}]:", block["description"])
        exec_block(block)
    

if __name__ == "__main__":
    main()
