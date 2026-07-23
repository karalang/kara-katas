package main

import "fmt"

// Benchmark workload for LeetCode #212 — Word Search II.
const ALPHA = 6
const SIZE = 12

func dfs(board, children, isEnd []int64, r, c, node int64) int64 {
	cell := board[r*SIZE+c]
	if cell == -1 {
		return 0
	}
	nxt := children[node*ALPHA+cell]
	if nxt == 0 {
		return 0
	}
	cnt := nxt // checksum each descended node
	if isEnd[nxt] == 1 {
		isEnd[nxt] = 0 // collect each word once per run
		cnt += nxt     // + collected-word identity
	}
	board[r*SIZE+c] = -1 // mark visited
	if r > 0 {
		cnt += dfs(board, children, isEnd, r-1, c, nxt)
	}
	if r+1 < SIZE {
		cnt += dfs(board, children, isEnd, r+1, c, nxt)
	}
	if c > 0 {
		cnt += dfs(board, children, isEnd, r, c-1, nxt)
	}
	if c+1 < SIZE {
		cnt += dfs(board, children, isEnd, r, c+1, nxt)
	}
	board[r*SIZE+c] = cell // restore
	return cnt
}

func main() {
	var nwords int64 = 4000
	var runs int64 = 40000
	var cells int64 = SIZE * SIZE

	children := make([]int64, ALPHA) // root at index 0
	isEnd0 := []int64{0}

	var state int64 = 12345

	// Build trie once.
	for w := int64(0); w < nwords; w++ {
		state = (state*1103515245 + 12345) & 2147483647
		length := 5 + state%4 // 5..8
		var cur int64 = 0
		for k := int64(0); k < length; k++ {
			state = (state*1103515245 + 12345) & 2147483647
			ch := state % ALPHA
			nxt := children[cur*ALPHA+ch]
			if nxt == 0 {
				idx := int64(len(isEnd0))
				for a := 0; a < ALPHA; a++ {
					children = append(children, 0)
				}
				isEnd0 = append(isEnd0, 0)
				children[cur*ALPHA+ch] = idx
				cur = idx
			} else {
				cur = nxt
			}
		}
		isEnd0[cur] = 1
	}

	nnodes := int64(len(isEnd0))
	isEnd := make([]int64, nnodes)
	board := make([]int64, cells)

	var sink int64 = 0
	for run := int64(0); run < runs; run++ {
		copy(isEnd, isEnd0)
		// Fresh board each run from the ongoing PRNG stream.
		for bi := int64(0); bi < cells; bi++ {
			state = (state*1103515245 + 12345) & 2147483647
			board[bi] = state % ALPHA
		}
		var found int64 = 0
		for r := int64(0); r < SIZE; r++ {
			for c := int64(0); c < SIZE; c++ {
				found += dfs(board, children, isEnd, r, c, 0)
			}
		}
		sink += found
	}

	fmt.Println(sink)
}
