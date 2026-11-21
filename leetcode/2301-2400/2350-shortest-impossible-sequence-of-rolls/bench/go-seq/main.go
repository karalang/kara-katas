// LeetCode #2350: Shortest Impossible Sequence of Rolls -- the bench, the ★
// arm in Go: the rolls cut greedily into pieces that each hold every face,
// with a table of the faces seen in the current piece made afresh at its
// end.
package main

import "fmt"

func shortestSequence(rolls []int64, k int64) int64 {
	seen := make([]bool, k+1)
	distinct, pieces := int64(0), int64(0)
	for _, r := range rolls {
		if !seen[r] {
			seen[r] = true
			distinct++
			if distinct == k {
				pieces++
				distinct = 0
				seen = make([]bool, k+1)
			}
		}
	}
	return pieces + 1
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 10 arrays of 10^5 rolls, of dice with 2 to 10^4 faces
	faces := []int64{2, 3, 6, 10, 20, 50, 100, 1000, 3000, 10000}
	seed := int64(2350)
	arrays := make([][]int64, 10)
	for a := range arrays {
		arrays[a] = make([]int64, 100000)
		for i := range arrays[a] {
			high := nextRandom(&seed)
			arrays[a][i] = (high*32768+nextRandom(&seed))%faces[a] + 1
		}
	}
	check := int64(0)
	for p := int64(0); p < 50; p++ {
		for a := range arrays {
			check = (check*31 + shortestSequence(arrays[a], faces[a]) + p) % 1000000007
		}
	}
	fmt.Printf("50 passes over 10 arrays of 10^5 rolls: checksum %d\n", check)
}
