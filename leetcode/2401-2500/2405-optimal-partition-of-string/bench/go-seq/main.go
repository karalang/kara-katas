// LeetCode #2405: Optimal Partition of String -- the bench, the ★ arm in
// Go: greedy with a bitmask, a letter already in the current part
// starting the next one.

package main

import "fmt"

var seed int64 = 2405

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func partitionString(s string) int64 {
	parts, seen := int64(1), int64(0)
	for i := 0; i < len(s); i++ {
		bit := int64(1) << (s[i] - 'a')
		if seen&bit != 0 {
			parts++
			seen = 0
		}
		seen |= bit
	}
	return parts
}

func main() {
	strings := make([]string, 26)
	for i := range strings {
		b := make([]byte, 100000)
		for j := range b {
			b[j] = byte('a' + nextRandom()%(int64(i)+1))
		}
		strings[i] = string(b)
	}
	var check int64
	for p := int64(0); p < 50; p++ {
		for _, s := range strings {
			check = (check*31 + partitionString(s) + p) % 1000000007
		}
	}
	fmt.Printf("50 passes over 26 strings of 10^5 letters: checksum %d\n", check)
}
