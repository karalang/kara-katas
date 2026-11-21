// LeetCode #2349: Design a Number Container System -- the bench, the ★ arm
// in Go: a map from each index to its number, and for each number a
// min-first binary heap of every index ever given it, popped lazily by
// find.
package main

import "fmt"

type minHeap []int64

func (h *minHeap) push(x int64) {
	*h = append(*h, x)
	a := *h
	i := len(a) - 1
	for i > 0 {
		p := (i - 1) / 2
		if a[p] <= a[i] {
			break
		}
		a[p], a[i] = a[i], a[p]
		i = p
	}
}

func (h *minHeap) pop() {
	a := *h
	n := len(a) - 1
	a[0] = a[n]
	a = a[:n]
	i := 0
	for {
		l, r, m := 2*i+1, 2*i+2, i
		if l < n && a[l] < a[m] {
			m = l
		}
		if r < n && a[r] < a[m] {
			m = r
		}
		if m == i {
			break
		}
		a[m], a[i] = a[i], a[m]
		i = m
	}
	*h = a
}

type numberContainers struct {
	at    map[int64]int64
	heaps map[int64]*minHeap
}

func newNumberContainers() *numberContainers {
	return &numberContainers{at: map[int64]int64{}, heaps: map[int64]*minHeap{}}
}

func (c *numberContainers) change(index, number int64) {
	c.at[index] = number
	h, ok := c.heaps[number]
	if !ok {
		h = &minHeap{}
		c.heaps[number] = h
	}
	h.push(index)
}

func (c *numberContainers) find(number int64) int64 {
	h, ok := c.heaps[number]
	if !ok {
		return -1
	}
	for len(*h) > 0 {
		top := (*h)[0]
		if c.at[top] == number {
			return top
		}
		h.pop()
	}
	return -1
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// two changes to every find, over 10^5 indices and 1000 numbers
	seed := int64(2349)
	type call struct{ kind, a, b int64 }
	calls := make([]call, 0, 200000)
	for i := 0; i < 200000; i++ {
		if nextRandom(&seed)%3 < 2 {
			high := nextRandom(&seed)
			index := (high*32768+nextRandom(&seed))%100000 + 1
			calls = append(calls, call{0, index, nextRandom(&seed)%1000 + 1})
		} else {
			calls = append(calls, call{1, nextRandom(&seed)%1000 + 1, 0})
		}
	}
	check := int64(0)
	for p := int64(0); p < 20; p++ {
		c := newNumberContainers()
		for _, k := range calls {
			if k.kind == 0 {
				c.change(k.a, k.b)
			} else {
				check = (check*31 + c.find(k.a) + p + 2) % 1000000007
			}
		}
	}
	fmt.Printf("20 passes over 2 * 10^5 calls: checksum %d\n", check)
}
