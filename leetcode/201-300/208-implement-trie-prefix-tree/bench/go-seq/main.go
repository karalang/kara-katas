package main

import "fmt"

// Benchmark workload for LeetCode #208 — Implement Trie (Prefix Tree).
const ALPHA = 5

func main() {
	var nwords int64 = 30000
	var nquery int64 = 8000000

	children := make([]int64, ALPHA) // root at index 0
	isEnd := []int64{0}

	var state int64 = 12345

	// Build phase.
	for w := int64(0); w < nwords; w++ {
		state = (state*1103515245 + 12345) & 2147483647
		length := 2 + state%7
		var cur int64 = 0
		for k := int64(0); k < length; k++ {
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
	var sink int64 = 0
	for q := int64(0); q < nquery; q++ {
		state = (state*1103515245 + 12345) & 2147483647
		length := 2 + state%7
		var cur int64 = 0
		alive := true
		for k := int64(0); k < length; k++ {
			state = (state*1103515245 + 12345) & 2147483647
			c := state % ALPHA
			if alive {
				nxt := children[cur*ALPHA+c]
				if nxt == 0 {
					alive = false
				} else {
					cur = nxt
				}
			}
		}
		if alive {
			sink += 1
			if isEnd[cur] == 1 {
				sink += 2
			}
		}
	}

	fmt.Println(sink)
}
