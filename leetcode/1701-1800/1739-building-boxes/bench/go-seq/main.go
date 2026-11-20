// LeetCode #1739: Building Boxes -- the bench (boxes.kara in Go): the
// staircase layer by layer, then the floor a box at a time.
package main

import "fmt"

func minimumBoxes(n32 int32) int32 {
	n := int64(n32)
	var placed, side int64
	for placed+(side+1)*(side+2)/2 <= n {
		side++
		placed += side * (side + 1) / 2
	}
	floor := side * (side + 1) / 2
	var extra int64
	for placed < n {
		extra++
		floor++
		placed += extra
	}
	return int32(floor)
}

var seed int64 = 1739

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	count, rounds := 20000, 15
	counts := make([]int32, count)
	for i := range counts {
		counts[i] = int32(wide()%1000000000 + 1)
	}
	var sum, check int64
	for r := 0; r < rounds; r++ {
		for _, n := range counts {
			answer := int64(minimumBoxes(n))
			sum += answer
			check = (check*31 + answer + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d counts up to 1000000000, %d rounds: floors sum to %d, checksum %d\n", count, rounds, sum, check)
}
