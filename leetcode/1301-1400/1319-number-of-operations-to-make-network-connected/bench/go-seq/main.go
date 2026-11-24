// LeetCode #1319 bench, Go mirror of the Kāra bench: the ★ arm (union-find
// with halved paths and the smaller group hung under the larger) on 4
// networks of 10^5 computers built once; then 25 passes, each moving one
// cable of every network to a pair chosen by the checksum so far,
// answering it and folding the answer plus the pass into the checksum.
package main

import "fmt"

func find(parent []int64, x int64) int64 {
	at := x
	for parent[at] != at {
		parent[at] = parent[parent[at]]
		at = parent[at]
	}
	return at
}

func makeConnected(n int64, connections [][]int64) int64 {
	if int64(len(connections)) < n-1 {
		return -1
	}
	parent := make([]int64, n)
	size := make([]int64, n)
	for i := range parent {
		parent[i] = int64(i)
		size[i] = 1
	}
	groups := n
	for _, c := range connections {
		a := find(parent, c[0])
		b := find(parent, c[1])
		if a != b {
			big, small := a, b
			if size[a] < size[b] {
				big, small = b, a
			}
			parent[small] = big
			size[big] += size[small]
			groups--
		}
	}
	return groups - 1
}

var seed int64 = 1319

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide(k int64) int64 {
	hi := nextRandom()
	return (hi*32768 + nextRandom()) % k
}

func main() {
	const n = 100000
	nets := make([][][]int64, 4)
	for kind := 0; kind < 4; kind++ {
		var cables [][]int64
		if kind == 1 {
			for i := int64(1); i < n; i++ {
				cables = append(cables, []int64{i - 1, i})
			}
			for k := len(cables) - 1; k >= 1; k-- {
				j := wide(int64(k + 1))
				cables[k], cables[j] = cables[j], cables[k]
			}
		} else if kind == 2 {
			for g := int64(0); g < n/10; g++ {
				for u := int64(0); u < 10; u++ {
					cables = append(cables, []int64{10*g + u, 10*g + (u+1)%10})
				}
			}
		} else {
			m := n
			if kind == 3 {
				m = n - 1
			}
			for len(cables) < m {
				u := wide(n)
				v := wide(n)
				if u != v {
					cables = append(cables, []int64{u, v})
				}
			}
		}
		nets[kind] = cables
	}
	var check int64
	for pass := int64(0); pass < 25; pass++ {
		for t := 0; t < 4; t++ {
			cables := nets[t]
			m := int64(len(cables))
			u := check % n
			v := (u + 1 + (check/7)%(n-1)) % n
			cables[check%m] = []int64{u, v}
			got := makeConnected(n, cables)
			check = (check*31 + got + 1 + pass) % 1000000007
		}
	}
	fmt.Printf("25 passes over 4 networks of 10^5: checksum %d\n", check)
}
