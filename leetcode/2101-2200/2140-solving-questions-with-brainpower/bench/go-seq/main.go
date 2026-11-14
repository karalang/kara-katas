// LeetCode #2140: Solving Questions With Brainpower -- the benchmark, the
// same algorithm as brainpower.kara.
package main

import "fmt"

func mostPoints(questions [][]int64) int64 {
	n := int64(len(questions))
	best := make([]int64, n+1)
	for i := n - 1; i >= 0; i-- {
		next := i + 1 + questions[i][1]
		if next > n {
			next = n
		}
		best[i] = best[i+1]
		if solve := questions[i][0] + best[next]; solve > best[i] {
			best[i] = solve
		}
	}
	return best[0]
}

var seed int64 = 2140

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][][]int64, 10)
	for l := range lists {
		lists[l] = make([][]int64, 100000)
		for i := range lists[l] {
			points := nextRandom()%100000 + 1
			brainpower := nextRandom() % 21
			lists[l][i] = []int64{points, brainpower}
		}
	}
	total, check := int64(0), int64(0)
	for round := int64(0); round < 20; round++ {
		for l := 0; l < 10; l++ {
			hi := nextRandom()
			at := (hi*32768 + nextRandom()) % 100000
			lists[l][at][0] = nextRandom()%100000 + 1
			lists[l][at][1] = nextRandom() % 21
			points := mostPoints(lists[l])
			total += points
			check = (check*31 + points + round) % 1000000007
		}
	}
	fmt.Printf("200 solves: %d points in all, checksum %d\n", total, check)
}
