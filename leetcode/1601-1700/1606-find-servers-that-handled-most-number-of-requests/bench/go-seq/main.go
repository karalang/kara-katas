// LeetCode #1606: Find Servers That Handled Most Number of Requests -- the
// bench in Go, mirroring servers.kara. Go has no ordered set, so the free
// servers are a segment tree of counts (first free at or after start); the
// busy ones are a binary min-heap of (time free, server).
package main

import "fmt"

type busy struct {
	t int64
	s int
}

type servers struct {
	size int
	tree []int
	heap []busy
}

func (sv *servers) set(s, v int) {
	node := sv.size + s
	sv.tree[node] = v
	for node /= 2; node >= 1; node /= 2 {
		sv.tree[node] = sv.tree[2*node] + sv.tree[2*node+1]
	}
}

func (sv *servers) firstFrom(node, lo, hi, from int) int {
	if hi <= from || sv.tree[node] == 0 {
		return -1
	}
	if node >= sv.size {
		return lo
	}
	mid := (lo + hi) / 2
	if r := sv.firstFrom(2*node, lo, mid, from); r >= 0 {
		return r
	}
	return sv.firstFrom(2*node+1, mid, hi, from)
}

func less(a, b busy) bool { return a.t < b.t || (a.t == b.t && a.s < b.s) }

func (sv *servers) push(b busy) {
	sv.heap = append(sv.heap, b)
	h := sv.heap
	i := len(h) - 1
	for i > 0 {
		p := (i - 1) / 2
		if !less(h[i], h[p]) {
			break
		}
		h[i], h[p] = h[p], h[i]
		i = p
	}
}

func (sv *servers) pop() busy {
	h := sv.heap
	top := h[0]
	n := len(h) - 1
	h[0] = h[n]
	h = h[:n]
	i := 0
	for {
		l, r, m := 2*i+1, 2*i+2, i
		if l < n && less(h[l], h[m]) {
			m = l
		}
		if r < n && less(h[r], h[m]) {
			m = r
		}
		if m == i {
			break
		}
		h[i], h[m] = h[m], h[i]
		i = m
	}
	sv.heap = h
	return top
}

func busiestServers(k int, arrival, load []int32) []int {
	sv := &servers{size: 1}
	for sv.size < k {
		sv.size *= 2
	}
	sv.tree = make([]int, 2*sv.size)
	for s := 0; s < k; s++ {
		sv.tree[sv.size+s] = 1
	}
	for node := sv.size - 1; node >= 1; node-- {
		sv.tree[node] = sv.tree[2*node] + sv.tree[2*node+1]
	}
	handled := make([]int, k)
	for i := range arrival {
		now := int64(arrival[i])
		for len(sv.heap) > 0 && sv.heap[0].t <= now {
			sv.set(sv.pop().s, 1)
		}
		s := sv.firstFrom(1, 0, sv.size, i%k)
		if s < 0 {
			s = sv.firstFrom(1, 0, sv.size, 0)
		}
		if s >= 0 {
			sv.set(s, 0)
			sv.push(busy{now + int64(load[i]), s})
			handled[s]++
		}
	}
	most := 0
	for _, h := range handled {
		if h > most {
			most = h
		}
	}
	var out []int
	for s := 0; s < k; s++ {
		if handled[s] == most {
			out = append(out, s)
		}
	}
	return out
}

func main() {
	seed := int64(1606)
	nextRandom := func() int64 {
		seed = (seed*1103515245 + 12345) % 2147483648
		return seed / 65536
	}
	type problem struct{ arrival, load []int32 }
	var problems []problem
	for p := 0; p < 20; p++ {
		arrival := make([]int32, 0, 100000)
		load := make([]int32, 0, 100000)
		t := int64(0)
		for i := 0; i < 100000; i++ {
			t += nextRandom()%3 + 1
			arrival = append(arrival, int32(t))
			a := nextRandom()
			b := nextRandom()
			load = append(load, int32((a*32768+b)%30000+1))
		}
		problems = append(problems, problem{arrival, load})
	}
	check, busiest := int64(0), 0
	for _, pr := range problems {
		servers := busiestServers(10000, pr.arrival, pr.load)
		for _, s := range servers {
			check = (check*31 + int64(s) + 1) % 1000000007
		}
		busiest += len(servers)
	}
	fmt.Printf("20 problems of 10000 servers and 100000 requests: %d busiest, checksum %d\n", busiest, check)
}
