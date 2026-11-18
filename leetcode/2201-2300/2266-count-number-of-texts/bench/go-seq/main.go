// LeetCode #2266: Count Number of Texts -- Go mirror of the ★ arm
// (texts.kara): ways[i] adds ways[i - j] for each run of j equal presses
// ending at i, up to 3, or 4 on `7` and `9`. Output is byte-identical to
// texts.kara.
package main

import (
	"fmt"
	"strings"
)

const mod = 1000000007

func countTexts(keys string) int64 {
	n := len(keys)
	ways := make([]int64, n+1)
	ways[0] = 1
	for i := 1; i <= n; i++ {
		key := keys[i-1]
		most := 3
		if key == '7' || key == '9' {
			most = 4
		}
		for j := 1; j <= most && j <= i && keys[i-j] == key; j++ {
			ways[i] = (ways[i] + ways[i-j]) % mod
		}
	}
	return ways[n]
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2266

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	sets := []string{"2", "79", "234", "23456789"}
	var check int64
	for t := 0; t < 40; t++ {
		keys := sets[t%4]
		var b strings.Builder
		for i := 0; i < 100000; i++ {
			b.WriteByte(keys[nextRandom()%int64(len(keys))])
		}
		check = (check*31 + countTexts(b.String())) % 1000000007
	}
	fmt.Printf("40 strings of 10^5: checksum %d\n", check)
}
