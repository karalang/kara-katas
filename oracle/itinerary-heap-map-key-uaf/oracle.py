"""LeetCode 332 — Reconstruct Itinerary (reference oracle).

Same Hierholzer walk as the Kara version: sorted destination lists, a
per-airport cursor into them, and a post-order emission reversed at the end.
"""


def find_itinerary(tickets):
    adj = {}
    for src, dst in tickets:
        adj.setdefault(src, []).append(dst)
    for dests in adj.values():
        dests.sort()

    cursor = {}
    route = []

    def visit(airport):
        dests = adj.get(airport, [])
        while cursor.get(airport, 0) < len(dests):
            used = cursor.get(airport, 0)
            cursor[airport] = used + 1
            visit(dests[used])
        route.append(airport)

    visit("JFK")
    return route[::-1]


def show(tickets):
    print(" -> ".join(find_itinerary(tickets)))


def main():
    show([["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]])
    show([["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]])
    show([["JFK", "ATL"], ["JFK", "SFO"], ["ATL", "JFK"], ["ATL", "SFO"], ["SFO", "ATL"]])
    show([["JFK", "AAA"]])


if __name__ == "__main__":
    main()
