// LeetCode #2052: Minimum Cost to Separate Sentence Into Rows -- Go mirror
// of the ★ arm's benchmark (separate.kara): the same 600 sentences, the
// same dynamic programming from the end.
package main

import (
	"fmt"
	"math"
	"strings"
)

var seed int64 = 2052

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func minimumCost(sentence string, k int64) int64 {
	words := strings.Split(sentence, " ")
	n := len(words)
	lens := make([]int64, n)
	for i, w := range words {
		lens[i] = int64(len(w))
	}
	best := make([]int64, n+1)
	for i := n - 1; i >= 0; i-- {
		width := int64(-1)
		least := int64(math.MaxInt64)
		j := i
		for j < n && width+1+lens[j] <= k {
			width += 1 + lens[j]
			j++
			if j == n {
				least = 0
			} else if c := (k-width)*(k-width) + best[j]; c < least {
				least = c
			}
		}
		best[i] = least
	}
	return best[0]
}

func main() {
	letters := "abcdefghijklmnopqrstuvwxyz"
	var sum, check int64
	for t := int64(0); t < 600; t++ {
		var b strings.Builder
		for b.Len() < 4990 {
			if b.Len() > 0 {
				b.WriteByte(' ')
			}
			w := nextRandom()%10 + 1
			for i := int64(0); i < w; i++ {
				b.WriteByte(letters[nextRandom()%26])
			}
		}
		k := 20 + t%200*20
		cost := minimumCost(b.String(), k)
		sum += cost
		check = (check*31 + cost) % 1000000007
	}
	fmt.Printf("600 sentences: sum %d, checksum %d\n", sum, check)
}
