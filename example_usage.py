from client import MultiPaxosEngine

nodes = [MultiPaxosEngine(f"node_{i}", quorum_size=2) for i in range(3)]
leader = nodes[0]
ok = leader.propose(slot=1, value="TX: credit $500", nodes=nodes)

print(f"Proposal status: {ok}")
print(f"Leader committed slot 1: {leader.committed.get(1)}")
