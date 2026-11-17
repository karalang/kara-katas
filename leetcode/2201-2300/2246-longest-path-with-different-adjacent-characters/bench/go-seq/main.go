// LeetCode #2246: Longest Path With Different Adjacent Characters -- the
// benchmark's Go mirror of path.kara: child lists, breadth-first order
// taken back to front, each node's two longest chains through children
// of another letter.
package main

import "fmt"

func longestPath(parent []int64, s []byte) int64 {
	n := len(parent)
	children := make([][]int, n)
	for v := 1; v < n; v++ {
		children[parent[v]] = append(children[parent[v]], v)
	}
	order := []int{0}
	for next := 0; next < len(order); next++ {
		order = append(order, children[order[next]]...)
	}
	down := make([]int64, n)
	best := int64(1)
	for i := len(order) - 1; i >= 0; i-- {
		v := order[i]
		first, second := int64(0), int64(0)
		for _, c := range children[v] {
			if s[c] == s[v] {
				continue
			}
			if down[c] > first {
				second = first
				first = down[c]
			} else if down[c] > second {
				second = down[c]
			}
		}
		down[v] = first + 1
		if first+second+1 > best {
			best = first + second + 1
		}
	}
	return best
}

var seed int64 = 2246

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	check := int64(0)
	for t := 0; t < 40; t++ {
		parent := make([]int64, 100000)
		parent[0] = -1
		for v := int64(1); v < 100000; v++ {
			parent[v] = wideRandom() % v
		}
		s := make([]byte, 100000)
		for v := range s {
			s[v] = byte('a' + nextRandom()%26)
		}
		check = (check*31 + longestPath(parent, s)) % 1000000007
	}
	fmt.Printf("40 trees of 100000 nodes: checksum %d\n", check)
}
