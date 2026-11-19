// LeetCode #1641: Count Sorted Vowel Strings -- the bench's Go mirror: the
// ★ arm on 4000000 random n from 1 to 50, all drawn first.
package main

import "fmt"

func countVowelStrings(n int64) int64 {
	ending := [5]int64{1, 1, 1, 1, 1}
	for i := int64(1); i < n; i++ {
		for v := 1; v < 5; v++ {
			ending[v] += ending[v-1]
		}
	}
	var sum int64
	for _, e := range ending {
		sum += e
	}
	return sum
}

var seed int64 = 1641

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	ns := make([]int64, 4000000)
	for i := range ns {
		ns[i] = nextRandom()%50 + 1
	}
	var check, total int64
	for _, n := range ns {
		count := countVowelStrings(n)
		total += count
		check = (check*31 + count) % 1000000007
	}
	fmt.Printf("4000000 random n: counts sum to %d, checksum %d\n", total, check)
}
