// LeetCode #691: Stickers to Spell Word -- bench program, Go mirror of the ★ arm.
package main

import "fmt"

var seed int64 = 691

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord(length, alphabet int64) string {
	w := make([]byte, length)
	for i := range w {
		w[i] = byte('a' + nextRandom()%alphabet)
	}
	return string(w)
}

func minStickers(stickers []string, target string) int64 {
	t := []byte(target)
	m := len(t)
	full := (1 << m) - 1
	counts := make([][]int64, 0, len(stickers))
	for _, s := range stickers {
		c := make([]int64, 26)
		for i := 0; i < len(s); i++ {
			c[s[i]-'a']++
		}
		counts = append(counts, c)
	}
	dp := make([]int64, full+1)
	for i := range dp {
		dp[i] = -1
	}
	dp[0] = 0
	left := make([]int64, 26)
	for mask := 0; mask <= full; mask++ {
		if dp[mask] < 0 {
			continue
		}
		for _, c := range counts {
			copy(left, c)
			next := mask
			for i := 0; i < m; i++ {
				k := t[i] - 'a'
				if next&(1<<i) == 0 && left[k] > 0 {
					left[k]--
					next |= 1 << i
				}
			}
			if next != mask && (dp[next] < 0 || dp[mask]+1 < dp[next]) {
				dp[next] = dp[mask] + 1
			}
		}
	}
	return dp[full]
}

func main() {
	problems := 160
	var total, checksum int64
	for p := 0; p < problems; p++ {
		stickers := make([]string, 0, 50)
		for s := 0; s < 50; s++ {
			stickers = append(stickers, randomWord(10, 12))
		}
		target := randomWord(15, 12)
		r := minStickers(stickers, target)
		total += r
		checksum = (checksum*31 + r + 2) % 1000000007
	}
	fmt.Printf("%d problems of 50 stickers and a 15-letter target: %d stickers in all, checksum %d\n", problems, total, checksum)
}
