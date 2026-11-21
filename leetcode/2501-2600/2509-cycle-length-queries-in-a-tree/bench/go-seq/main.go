// LeetCode #2509: Cycle Length Queries in a Tree -- Go mirror of the
// benchmark (cycle.kara): the same queries, passes and checksum.
package main

import "fmt"

func cycleLengthQueries(n int64, queries [][2]int64) []int64 {
	answer := make([]int64, 0, len(queries))
	for _, q := range queries {
		a, b, length := q[0], q[1], int64(1)
		for a != b {
			if a > b {
				a /= 2
			} else {
				b /= 2
			}
			length++
		}
		answer = append(answer, length)
	}
	return answer
}

var seed int64 = 2509

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func below(top int64) int64 {
	hi := nextRandom()
	return (hi*32768 + nextRandom()) % top
}

func main() {
	const size = int64(1)<<30 - 1
	queries := make([][2]int64, 0, 100000)
	for len(queries) < 100000 {
		a := below(size) + 1
		b := below(size) + 1
		if a != b {
			queries = append(queries, [2]int64{a, b})
		}
	}
	const passes = 34
	var check int64
	for p := int64(0); p < passes; p++ {
		at := check % int64(len(queries))
		kept := queries[at][1]
		b := (check+p)%size + 1
		if b == queries[at][0] {
			b = b%size + 1
		}
		queries[at][1] = b
		for _, x := range cycleLengthQueries(30, queries) {
			check = (check*31 + x + p) % 1000000007
		}
		queries[at][1] = kept
	}
	fmt.Printf("%d passes over 10^5 queries on 30 levels: checksum %d\n", passes, check)
}
