// LeetCode #2729: Check if The Number is Fascinating -- the bench
// (fascinating.kara in Go): n, 2 n and 3 n joined by `fmt.Sprintf`, the
// digits sorted and compared with "123456789".
package main

import (
	"fmt"
	"sort"
)

func isFascinating(n int64) bool {
	joined := []byte(fmt.Sprintf("%d%d%d", n, 2*n, 3*n))
	sort.Slice(joined, func(a, b int) bool { return joined[a] < joined[b] })
	return string(joined) == "123456789"
}

var seed int64 = 2729

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count, rounds := 1000000, 5
	fascinating := []int64{192, 219, 273, 327}
	numbers := make([]int64, 0, count)
	for i := 0; i < count; i++ {
		if i%50 == 0 {
			numbers = append(numbers, fascinating[nextRandom()%4])
		} else {
			numbers = append(numbers, nextRandom()%900+100)
		}
	}
	var yes, check int64
	for r := 0; r < rounds; r++ {
		for _, n := range numbers {
			answer := isFascinating(n)
			v := int64(1)
			if answer {
				yes++
				v = 2
			}
			check = (check*31 + v + int64(r)) % 1000000007
		}
	}
	fmt.Printf("%d numbers, %d rounds: %d fascinating, checksum %d\n", count, rounds, yes, check)
}
