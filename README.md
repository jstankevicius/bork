# minible

An incredibly simple Python utility that just runs a bunch of commands on some
number of servers. The `config.yaml` file should be pretty self-explanatory: the
user simply defines execution "blocks" which are run one after another. Each set
of commands is executed in parallel across all nodes.
