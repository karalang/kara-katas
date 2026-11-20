// LeetCode #1239: the benchmark, mirroring the Kāra file.
package main

import (
	"fmt"
	"math/bits"
)

var seed int64 = 1239

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func maskOf(word string) (int64, bool) {
	var mask int64
	for i := 0; i < len(word); i++ {
		bit := int64(1) << (word[i] - 97)
		if mask&bit != 0 {
			return 0, false
		}
		mask |= bit
	}
	return mask, true
}

func search(masks []int64, at int, taken int64) int64 {
	if at == len(masks) {
		return int64(bits.OnesCount64(uint64(taken)))
	}
	best := search(masks, at+1, taken)
	if taken&masks[at] == 0 {
		if t := search(masks, at+1, taken|masks[at]); t > best {
			best = t
		}
	}
	return best
}

func maxLength(arr []string) int64 {
	masks := []int64{}
	for _, w := range arr {
		if m, ok := maskOf(w); ok {
			masks = append(masks, m)
		}
	}
	return search(masks, 0, 0)
}

func main() {
	lists := make([][]string, 0, 20000)
	for l := 0; l < 20000; l++ {
		words := make([]string, 0, 16)
		for k := 0; k < 16; k++ {
			n := nextRandom()%2 + 1
			w := make([]byte, n)
			for i := range w {
				w[i] = byte('a' + nextRandom()%26)
			}
			words = append(words, string(w))
		}
		lists = append(lists, words)
	}
	var total, check int64
	for _, words := range lists {
		best := maxLength(words)
		total += best
		check = (check*131 + best) % 1000000007
	}
	fmt.Printf("20000 lists of 16 words: total %d, checksum %d\n", total, check)
}
