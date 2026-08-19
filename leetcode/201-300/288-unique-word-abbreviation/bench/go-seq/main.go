// Benchmark twin for LeetCode #288 — same algorithm as uniqueabbr.kara.
package main

import (
	"fmt"
	"strconv"
)

// Sole holds the single word; conflicted marks two-or-more.
type bucket struct {
	word       string
	conflicted bool
}

func abbrev(w string) string {
	n := len(w)
	if n <= 2 {
		return w
	}
	return string(w[0]) + strconv.Itoa(n-2) + string(w[n-1])
}

func nextRand(state int64) int64 {
	return (state*1103515245 + 12345) & 2147483647
}

func main() {
	const letters = "abcdefghijklmnopqrstuvwxyz"
	var dictN, poolN, punches int64 = 3000, 20000, 1000000
	var seed int64 = 12345

	dict := make([]string, 0, dictN)
	for i := int64(0); i < dictN; i++ {
		seed = nextRand(seed)
		n := 3 + ((seed / 65536) % 8)
		buf := make([]byte, 0, n)
		for j := int64(0); j < n; j++ {
			seed = nextRand(seed)
			buf = append(buf, letters[(seed/65536)%26])
		}
		dict = append(dict, string(buf))
	}

	idx := make(map[string]bucket)
	for _, w := range dict {
		a := abbrev(w)
		prev, ok := idx[a]
		if !ok {
			idx[a] = bucket{word: w}
		} else if !prev.conflicted && prev.word != w {
			idx[a] = bucket{conflicted: true}
		}
	}

	pool := make([]string, 0, poolN)
	for i := int64(0); i < poolN; i++ {
		if i%2 == 0 {
			pool = append(pool, dict[(i*7)%dictN])
		} else {
			seed = nextRand(seed)
			n := 3 + ((seed / 65536) % 8)
			buf := make([]byte, 0, n)
			for j := int64(0); j < n; j++ {
				seed = nextRand(seed)
				buf = append(buf, letters[(seed/65536)%26])
			}
			pool = append(pool, string(buf))
		}
	}

	var uniqueCount int64
	for i := int64(0); i < punches; i++ {
		word := pool[i%poolN]
		a := abbrev(word)
		hit, ok := idx[a]
		u := false
		if !ok {
			u = true
		} else if !hit.conflicted {
			u = hit.word == word
		}
		if u {
			uniqueCount++
		}
	}
	fmt.Printf("unique %d\n", uniqueCount)
}
