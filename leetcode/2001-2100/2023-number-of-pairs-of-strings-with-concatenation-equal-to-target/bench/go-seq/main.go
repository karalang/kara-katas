// LeetCode #2023: Number of Pairs of Strings With Concatenation Equal to
// Target -- the ★ arm in Go, the same algorithm and workload as pairs.kara.
package main

import (
	"fmt"
	"strings"
)

func numOfPairs(nums []string, target string) int64 {
	count := map[string]int64{}
	for _, s := range nums {
		count[s]++
	}
	var pairs int64
	for k := 1; k < len(target); k++ {
		a := target[:k]
		b := target[k:]
		ca := count[a]
		if a == b {
			pairs += ca * (ca - 1)
		} else {
			pairs += ca * count[b]
		}
	}
	return pairs
}

var seed int64 = 2023

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][]string, 0, 300)
	targets := make([]string, 0, 300)
	for p := 0; p < 300; p++ {
		blockLen := nextRandom()%3 + 1
		var sb strings.Builder
		for i := int64(0); i < blockLen; i++ {
			sb.WriteByte(byte('1' + nextRandom()%2))
		}
		block := sb.String()
		nums := make([]string, 100)
		for i := range nums {
			nums[i] = strings.Repeat(block, int(nextRandom()%(100/blockLen)+1))
		}
		lists = append(lists, nums)
		targets = append(targets, strings.Repeat(block, int(nextRandom()%(100/blockLen-1)+2)))
	}
	var calls, total, check int64
	for r := 0; r < 20; r++ {
		for p := 0; p < 300; p++ {
			pairs := numOfPairs(lists[p], targets[p])
			calls++
			total += pairs
			check = (check*31 + pairs) % 1000000007
		}
	}
	fmt.Printf("%d calls: %d pairs, checksum %d\n", calls, total, check)
}
