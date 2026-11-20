// LeetCode #1732: Find the Highest Altitude -- the bench (altitude.kara):
// the altitudes listed, then the largest.
package main

import "fmt"

func largestAltitude(gain []int32) int32 {
	altitudes := []int32{0}
	for _, g := range gain {
		altitudes = append(altitudes, altitudes[len(altitudes)-1]+g)
	}
	highest := altitudes[0]
	for _, a := range altitudes[1:] {
		highest = max(highest, a)
	}
	return highest
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := 1000
	var rounds int64 = 2000
	n := 100
	var seed int64 = 1732
	trips := make([][]int32, count)
	for c := range trips {
		trips[c] = make([]int32, n)
		for i := range trips[c] {
			trips[c][i] = int32(nextRandom(&seed)%201 - 100)
		}
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, gain := range trips {
			answer := int64(largestAltitude(gain))
			sum += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d trips of %d gains, %d rounds: highest points sum to %d, checksum %d\n", count, n, rounds, sum, check)
}
