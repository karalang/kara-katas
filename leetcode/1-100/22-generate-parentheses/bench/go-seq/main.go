// Bench mirror of backtracking.kara — same owned-snapshot recursive
// backtracking (cur + "(" allocates a fresh string per node), same
// K x n=10 full-set generation, same total-bytes sink.
package main

import "fmt"

func backtrack(cur string, open, close, n int, out *[]string) {
	if close == n {
		*out = append(*out, cur)
		return
	}
	if open < n {
		backtrack(cur+"(", open+1, close, n, out)
	}
	if close < open {
		backtrack(cur+")", open, close+1, n, out)
	}
}

func generateParenthesis(n int) []string {
	out := make([]string, 0)
	backtrack("", 0, 0, n, &out)
	return out
}

func main() {
	const n = 10
	const iters = 150
	var total uint64
	for k := 0; k < iters; k++ {
		combos := generateParenthesis(n)
		var bytes uint64
		for _, c := range combos {
			bytes += uint64(len(c))
		}
		total += bytes
	}
	fmt.Println(total) // 150 * 16796 * 20 = 50,388,000
}
