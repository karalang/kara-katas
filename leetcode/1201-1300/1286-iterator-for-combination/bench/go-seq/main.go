// LeetCode #1286 bench, in Go: the ★ arm (the masks with k bits, from the
// largest down) over every length of the 15 letters "abcdefghijklmno",
// 1000 rounds, every combination folded into a checksum.
package main

import (
	"fmt"
	"math/bits"
	"strings"
)

type CombinationIterator struct {
	chars []rune
	k     int
	mask  int64
}

func newIterator(characters string, k int64) *CombinationIterator {
	n := int64(len(characters))
	return &CombinationIterator{chars: []rune(characters), k: int(k), mask: ((int64(1) << k) - 1) << (n - k)}
}

func (it *CombinationIterator) Next() string {
	n := len(it.chars)
	var out strings.Builder
	for i := 0; i < n; i++ {
		if (it.mask>>(n-1-i))&1 == 1 {
			out.WriteRune(it.chars[i])
		}
	}
	it.mask--
	for it.mask > 0 && bits.OnesCount64(uint64(it.mask)) != it.k {
		it.mask--
	}
	return out.String()
}

func (it *CombinationIterator) HasNext() bool { return it.mask > 0 }

func main() {
	var check int64
	for round := int64(0); round < 1000; round++ {
		for k := int64(1); k < 16; k++ {
			it := newIterator("abcdefghijklmno", k)
			for it.HasNext() {
				s := it.Next()
				for i := 0; i < len(s); i++ {
					check = (check*131 + int64(s[i]) + round) % 1000000007
				}
			}
		}
	}
	fmt.Printf("1000 rounds of every length of 15 letters: checksum %d\n", check)
}
