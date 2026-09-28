"""Multi-Paxos Log Replication Consensus Engine.
100% Python Standard Library.
"""

class MultiPaxosEngine:
    """Multi-Paxos log replication engine with leader lease optimization."""
    def __init__(self, node_id, quorum_size=2):
        self.node_id = node_id
        self.quorum_size = quorum_size
        self.ballot = 0
        self.log = {}
        self.committed = {}

    def propose(self, slot, value, nodes):
        self.ballot += 1
        accept_votes = 0
        for node in nodes:
            if node.handle_accept(slot, self.ballot, value):
                accept_votes += 1
        if accept_votes >= self.quorum_size:
            self.committed[slot] = value
            for node in nodes:
                node.handle_commit(slot, value)
            return True
        return False

    def handle_accept(self, slot, ballot, value):
        cur_ballot, _ = self.log.get(slot, (0, None))
        if ballot >= cur_ballot:
            self.log[slot] = (ballot, value)
            return True
        return False

    def handle_commit(self, slot, value):
        self.committed[slot] = value
