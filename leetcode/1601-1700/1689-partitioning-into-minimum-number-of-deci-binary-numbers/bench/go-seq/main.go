// LeetCode #1689: Partitioning Into Minimum Number Of Deci-Binary Numbers
// -- the bench's Go mirror: the ★ arm on 100 random numbers of 100000
// digits, all drawn first, each answered 50 times.
package main

import (
	"fmt"
	"strings"
)

func minPartitions(n string) int32 {
	var largest byte
	for i := 0; i < len(n); i++ {
		if d := n[i] - '0'; d > largest {
			largest = d
		}
	}
	return int32(largest)
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1689

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, size, rounds = 100, 100000, 50
	const digits = "0123456789"
	numbers := make([]string, 0, count)
	for c := 0; c < count; c++ {
		top := nextRandom()%9 + 1
		var n strings.Builder
		n.Grow(size)
		n.WriteByte(digits[nextRandom()%top+1])
		for i := 1; i < size; i++ {
			n.WriteByte(digits[nextRandom()%(top+1)])
		}
		numbers = append(numbers, n.String())
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, n := range numbers {
			answer := int64(minPartitions(n))
			total += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d numbers of %d digits, %d rounds: answers sum to %d, checksum %d\n", count, size, rounds, total, check)
}
