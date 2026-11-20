// LeetCode #1748: Sum of Unique Elements -- the bench (unique.kara in Go):
// one pass with a state per value.
package main

import "fmt"

func sumOfUnique(nums []int32) int32 {
	var seen [101]int64
	var sum int32
	for _, x := range nums {
		if seen[x] == 0 {
			sum += x
		} else if seen[x] == 1 {
			sum -= x
		}
		seen[x] = min(seen[x]+1, 2)
	}
	return sum
}

var seed int64 = 1748

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds, n = 50000, 10, 100
	arrays := make([][]int32, count)
	for c := range arrays {
		arrays[c] = make([]int32, n)
		for i := range arrays[c] {
			arrays[c][i] = int32(nextRandom()%100 + 1)
		}
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range arrays {
			answer := int64(sumOfUnique(nums))
			sum += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d values, %d rounds: unique sums add to %d, checksum %d\n", count, n, rounds, sum, check)
}
