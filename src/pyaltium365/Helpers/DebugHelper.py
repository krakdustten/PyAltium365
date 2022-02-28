from typing import List, Dict, Any


def print_amount_of_parameters_in_list_dict(ip: List[Dict[str, Any]]) -> None:
    op: Dict[str, int] = {}
    for i in ip:
        for key in i:
            if key in op:
                op[key] += 1
            else:
                op[key] = 1
    for o, p in op.items():
        print(f"{o}: {p}")
