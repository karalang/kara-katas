// LeetCode #2268: Minimum Number of Keypresses -- the bench, the ★ arm.
package main

import (
	"fmt"
	"sort"
	"strings"
)

func minimumKeypresses(s string) int64 {
	count := make([]int64, 26)
	for i := 0; i < len(s); i++ {
		count[s[i]-'a']++
	}
	sort.Slice(count, func(a, b int) bool { return count[a] > count[b] })
	var total int64
	for i, c := range count {
		total += c * (int64(i)/9 + 1)
	}
	return total
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2268

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	ks := []int64{3, 10, 12, 26}
	var check int64
	for t := 0; t < 40; t++ {
		k := ks[t%4]
		var b strings.Builder
		for i := 0; i < 100000; i++ {
			b.WriteByte(byte('a' + nextRandom()%k))
		}
		check = (check*31 + minimumKeypresses(b.String())) % 1000000007
	}
	fmt.Printf("40 strings of 10^5: checksum %d\n", check)
}
