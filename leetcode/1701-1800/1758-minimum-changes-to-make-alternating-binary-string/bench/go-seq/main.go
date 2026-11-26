// LeetCode #1758: Minimum Changes To Make Alternating Binary String -- the
// bench in Go, mirroring min_operations.kara: one pass counting the
// characters that differ from "0101...".
package main

import (
	"fmt"
	"strings"
)

func minOperations(s string) int32 {
	differ := int64(0)
	for i := 0; i < len(s); i++ {
		if int64(s[i]-'0') != int64(i%2) {
			differ++
		}
	}
	return int32(min(differ, int64(len(s))-differ))
}

func main() {
	seed := int64(1758)
	list := make([]string, 0, 2000)
	for j := 0; j < 2000; j++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		n := 1 + seed/65536%20000
		seed = (seed*1103515245 + 12345) % 2147483648
		chance := seed / 65536 % 101
		var b strings.Builder
		for i := int64(0); i < n; i++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			if seed/65536%100 < chance {
				b.WriteByte('1')
			} else {
				b.WriteByte('0')
			}
		}
		list = append(list, b.String())
	}
	check := int64(0)
	for call := int64(0); call < 30000; call++ {
		s := list[(check+call*7919)%2000]
		check = (check*31 + int64(minOperations(s))) % 1000000007
	}
	fmt.Printf("30000 calls over 2000 strings: checksum %d\n", check)
}
