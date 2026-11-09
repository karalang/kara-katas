// LeetCode #2053: Kth Distinct String in an Array -- Go mirror of the ★
// arm's benchmark (distinct.kara): the same 5000 arrays, the same count
// into a map and walk of the array.
package main

import (
	"fmt"
	"strings"
)

var seed int64 = 2053

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func kthDistinct(arr []string, k int64) string {
	counts := map[string]int64{}
	for _, s := range arr {
		counts[s]++
	}
	left := k
	for _, s := range arr {
		if counts[s] == 1 {
			left--
			if left == 0 {
				return s
			}
		}
	}
	return ""
}

func main() {
	alphabet := "abcdefghijklmnopqrstuvwxyz"
	var found, check int64
	for t := int64(0); t < 5000; t++ {
		letters := 2 + t%25
		arr := make([]string, 0, 1000)
		for i := 0; i < 1000; i++ {
			n := nextRandom()%5 + 1
			var b strings.Builder
			for j := int64(0); j < n; j++ {
				b.WriteByte(alphabet[nextRandom()%letters])
			}
			arr = append(arr, b.String())
		}
		answer := kthDistinct(arr, t%1000+1)
		if len(answer) > 0 {
			found++
		}
		for _, ch := range answer {
			check = (check*31 + int64(ch)) % 1000000007
		}
		check = (check*31 + int64(len(answer)) + 1) % 1000000007
	}
	fmt.Printf("5000 arrays: %d answers found, checksum %d\n", found, check)
}
