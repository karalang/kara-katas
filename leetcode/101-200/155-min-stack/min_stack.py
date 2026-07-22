"""LeetCode 155 — Min Stack (Python mirror / oracle).

Parallel `mins` stack whose top is always the running minimum, so getMin is
O(1). Mirrors the Kāra version's operation sequence exactly.
"""


class MinStack:
    def __init__(self):
        self.data = []
        self.mins = []

    def push(self, x):
        self.data.append(x)
        if not self.mins or x <= self.mins[-1]:
            self.mins.append(x)
        else:
            self.mins.append(self.mins[-1])

    def pop(self):
        self.data.pop()
        self.mins.pop()

    def top(self):
        return self.data[-1]

    def get_min(self):
        return self.mins[-1]


def main():
    st = MinStack()
    st.push(-2)
    st.push(0)
    st.push(-3)
    print(st.get_min())
    st.pop()
    print(st.top())
    print(st.get_min())

    st.push(-5)
    print(st.get_min())
    print(st.top())
    st.pop()
    print(st.get_min())
    st.pop()
    print(st.top())
    print(st.get_min())


main()
