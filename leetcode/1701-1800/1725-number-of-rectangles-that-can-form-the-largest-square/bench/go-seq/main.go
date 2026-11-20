// LeetCode #1725: Number Of Rectangles That Can Form The Largest Square
// -- the bench (rectangles.kara): one pass, the largest shorter side so
// far and how many rectangles give it.
package main

import "fmt"

func countGoodRectangles(rectangles [][]int32) int32 {
	var best, count int32
	for _, r := range rectangles {
		side := min(r[0], r[1])
		if side > best {
			best = side
			count = 1
		} else if side == best {
			count++
		}
	}
	return count
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := 1000
	var rounds int64 = 50
	n := 1000
	var seed int64 = 1725
	problems := make([][][]int32, count)
	for c := range problems {
		problems[c] = make([][]int32, n)
		for i := range problems[c] {
			l := int32(nextRandom(&seed)%20 + 1)
			w := int32(nextRandom(&seed)%20 + 1)
			problems[c][i] = []int32{l, w}
		}
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, rectangles := range problems {
			answer := int64(countGoodRectangles(rectangles))
			sum += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d problems of %d rectangles, %d rounds: answers sum to %d, checksum %d\n", count, n, rounds, sum, check)
}
