"""Benchmark workload for LeetCode #155 — Min Stack (Python; scale lane)."""


class MinStack:
    def __init__(self):
        self.data = []
        self.mins = []


def ms_push(st, x):
    st.data.append(x)
    m = len(st.mins)
    if m == 0 or x <= st.mins[m - 1]:
        st.mins.append(x)
    else:
        st.mins.append(st.mins[m - 1])


def ms_pop(st):
    st.data.pop()
    st.mins.pop()


def ms_top(st):
    return st.data[len(st.data) - 1]


def ms_get_min(st):
    return st.mins[len(st.mins) - 1]


def main():
    ops = 90000000
    cap = 100000

    st = MinStack()
    state = 12345
    sz = 0
    sink = 0

    for _i in range(ops):
        state = (state * 1103515245 + 12345) & 2147483647
        op = (state // 1024) % 4
        if sz == 0:
            state = (state * 1103515245 + 12345) & 2147483647
            val = state % 2000000 - 1000000
            ms_push(st, val)
            sz += 1
        elif sz >= cap:
            ms_pop(st)
            sz -= 1
        elif op == 0:
            state = (state * 1103515245 + 12345) & 2147483647
            val = state % 2000000 - 1000000
            ms_push(st, val)
            sz += 1
        elif op == 1:
            ms_pop(st)
            sz -= 1
        elif op == 2:
            sink += ms_get_min(st)
        else:
            sink += ms_top(st)
    print(sink)


main()
