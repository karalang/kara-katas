// LeetCode #1769: Minimum Number of Operations to Move All Balls to Each
// Box -- the bench in Go, mirroring min_operations.kara: two sweeps over
// the row's bytes.
package main

import (
	"fmt"
	"strings"
)

func minOperations(boxes string) []int32 {
	n := len(boxes)
	answer := make([]int32, n)
	var balls, moves int32
	for i := 0; i < n; i++ {
		answer[i] += moves
		if boxes[i] == '1' {
			balls++
		}
		moves += balls
	}
	balls, moves = 0, 0
	for i := n - 1; i >= 0; i-- {
		answer[i] += moves
		if boxes[i] == '1' {
			balls++
		}
		moves += balls
	}
	return answer
}

var seed int64 = 1769

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rows := make([]string, 200)
	for r := range rows {
		full := nextRandom() % 101
		var b strings.Builder
		for i := 0; i < 2000; i++ {
			if nextRandom()%100 < full {
				b.WriteByte('1')
			} else {
				b.WriteByte('0')
			}
		}
		rows[r] = b.String()
	}
	var check int64
	for call := int64(0); call < 40000; call++ {
		answer := minOperations(rows[(check+call*7919)%200])
		check = (check*31 + int64(answer[check%2000])) % 1000000007
	}
	fmt.Printf("40000 calls over 200 rows: checksum %d\n", check)
}
