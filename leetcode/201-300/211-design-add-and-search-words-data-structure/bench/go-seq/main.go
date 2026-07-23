package main

import "fmt"

// Benchmark workload for LeetCode #211 — Add and Search Words Data Structure.
const ALPHA = 6
const WLEN = 6

func dfs(children, isEnd, wild, letter []int64, cur int64, pos int) bool {
	if pos == WLEN {
		return isEnd[cur] == 1
	}
	if wild[pos] == 1 {
		for a := int64(0); a < ALPHA; a++ {
			nc := children[cur*ALPHA+a]
			if nc != 0 && dfs(children, isEnd, wild, letter, nc, pos+1) {
				return true
			}
		}
		return false
	}
	nc := children[cur*ALPHA+letter[pos]]
	if nc == 0 {
		return false
	}
	return dfs(children, isEnd, wild, letter, nc, pos+1)
}

func main() {
	var nwords int64 = 20000
	var nquery int64 = 8000000

	children := make([]int64, ALPHA) // root at index 0
	isEnd := []int64{0}

	var state int64 = 12345

	// Build phase.
	for w := int64(0); w < nwords; w++ {
		var cur int64 = 0
		for k := 0; k < WLEN; k++ {
			state = (state*1103515245 + 12345) & 2147483647
			c := state % ALPHA
			nxt := children[cur*ALPHA+c]
			if nxt == 0 {
				idx := int64(len(isEnd))
				for a := 0; a < ALPHA; a++ {
					children = append(children, 0)
				}
				isEnd = append(isEnd, 0)
				children[cur*ALPHA+c] = idx
				cur = idx
			} else {
				cur = nxt
			}
		}
		isEnd[cur] = 1
	}

	// Query phase.
	wild := make([]int64, WLEN)
	letter := make([]int64, WLEN)
	var sink int64 = 0
	for q := int64(0); q < nquery; q++ {
		for k := 0; k < WLEN; k++ {
			state = (state*1103515245 + 12345) & 2147483647
			v := state
			if v%6 == 0 {
				wild[k] = 1
			} else {
				wild[k] = 0
			}
			letter[k] = (v / 6) % ALPHA
		}
		if dfs(children, isEnd, wild, letter, 0, 0) {
			sink += 1
		}
	}

	fmt.Println(sink)
}
