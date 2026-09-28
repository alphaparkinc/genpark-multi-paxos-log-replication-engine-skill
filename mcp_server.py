import sys
import json
from client import MultiPaxosEngine

nodes = [MultiPaxosEngine(f"n_{i}", quorum_size=2) for i in range(3)]

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "multi_paxos_propose",
                        "description": "Propose value for log slot in Multi-Paxos consensus cluster",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "slot": {"type": "integer"},
                                "value": {"type": "string"}
                            },
                            "required": ["slot", "value"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "multi_paxos_propose":
            ok = nodes[0].propose(args["slot"], args["value"], nodes)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"slot": args["slot"], "committed": ok, "value": args["value"]})}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if line.strip():
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
