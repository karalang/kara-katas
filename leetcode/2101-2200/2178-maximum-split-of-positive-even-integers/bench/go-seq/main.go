// LeetCode #2178: Maximum Split of Positive Even Integers -- the
// benchmark's Go mirror of split.kara.
package main

import "fmt"

func maximumEvenSplit(finalSum int64) []int64 {
	parts := []int64{}
	if finalSum%2 != 0 {
		return parts
	}
	left := finalSum
	next := int64(2)
	for left >= next {
		parts = append(parts, next)
		left -= next
		next += 2
	}
	parts[len(parts)-1] += left
	return parts
}

var seed int64 = 2178

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	partsInAll := 0
	var check int64
	for r := 0; r < 400; r++ {
		a := nextRandom()
		b := nextRandom()
		c := nextRandom()
		finalSum := ((a*32768+b)*32768+c)%10000000000 + 1
		parts := maximumEvenSplit(finalSum)
		partsInAll += len(parts)
		for _, p := range parts {
			check = (check*31 + p) % 1000000007
		}
	}
	fmt.Printf("400 solves: %d parts, checksum %d\n", partsInAll, check)
}
