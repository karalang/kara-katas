// LeetCode #2086: Minimum Number of Food Buckets to Feed the Hamsters --
// Go mirror of the ★ arm's benchmark (bucket.kara): the same street and
// 3000 windows, each a substring of the street, served by the same greedy.
package main

import (
	"fmt"
	"strings"
)

var seed int64 = 2086

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func minimumBuckets(hamsters string) int64 {
	n := len(hamsters)
	bucket := make([]bool, n)
	var count int64
	for i := 0; i < n; i++ {
		if hamsters[i] != 'H' {
			continue
		}
		if i > 0 && bucket[i-1] {
			continue
		}
		if i+1 < n && hamsters[i+1] == '.' {
			bucket[i+1] = true
			count++
		} else if i > 0 && hamsters[i-1] == '.' {
			bucket[i-1] = true
			count++
		} else {
			return -1
		}
	}
	return count
}

func main() {
	pieces := []string{".", "H.", ".H", "H.H", ".H.H.", "..H"}
	var b strings.Builder
	for b.Len() < 1000000 {
		b.WriteString(pieces[nextRandom()%6])
	}
	street := b.String()
	var total, impossible, check int64
	for k := 0; k < 3000; k++ {
		hi := nextRandom()
		from := (hi*32768 + nextRandom()) % 900000
		a := minimumBuckets(street[from : from+100000])
		if a < 0 {
			impossible++
		} else {
			total += a
		}
		check = (check*31 + a + 1) % 1000000007
	}
	fmt.Printf("3000 windows: sum %d, %d impossible, checksum %d\n", total, impossible, check)
}
