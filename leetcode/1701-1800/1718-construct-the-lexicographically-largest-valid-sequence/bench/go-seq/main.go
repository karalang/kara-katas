// LeetCode #1718: Construct the Lexicographically Largest Valid Sequence
// -- the bench (sequence.kara): the first empty slot filled with the
// largest number that fits, backtracking when none does.
package main

import "fmt"

func place(seq []int32, used []bool, at int, n int32) bool {
	for at < len(seq) && seq[at] != 0 {
		at++
	}
	if at == len(seq) {
		return true
	}
	for v := n; v >= 1; v-- {
		u := int(v)
		if used[u] {
			continue
		}
		if v > 1 && (at+u >= len(seq) || seq[at+u] != 0) {
			continue
		}
		used[u] = true
		seq[at] = v
		if v > 1 {
			seq[at+u] = v
		}
		if place(seq, used, at+1, n) {
			return true
		}
		used[u] = false
		seq[at] = 0
		if v > 1 {
			seq[at+u] = 0
		}
	}
	return false
}

func constructDistancedSequence(n int32) []int32 {
	seq := make([]int32, 2*n-1)
	used := make([]bool, n+1)
	place(seq, used, 0, n)
	return seq
}

func main() {
	var rounds int64 = 2000
	var values, check int64
	for r := int64(0); r < rounds; r++ {
		for n := int32(1); n <= 20; n++ {
			for _, v := range constructDistancedSequence(n) {
				values++
				check = (check*31 + int64(v) + r) % 1000000007
			}
		}
	}
	fmt.Printf("every n from 1 to 20, %d rounds: %d values, checksum %d\n", rounds, values, check)
}
