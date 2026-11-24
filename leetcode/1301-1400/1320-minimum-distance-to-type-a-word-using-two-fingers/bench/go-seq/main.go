// LeetCode #1320 bench, Go mirror of the Kāra bench: the ★ arm (one row of
// 27 for the other finger's key, carried from letter to letter) on 100
// words of 300 letters over 2, 5 or 26 letters, built once; then 80
// passes, each setting one letter of every word from the checksum so far,
// answering it and folding the answer plus the pass into the checksum.
package main

import "fmt"

func abs(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

func keyDistance(a, b int64) int64 {
	if a == 26 {
		return 0
	}
	return abs(a/6-b/6) + abs(a%6-b%6)
}

func minimumDistance(word string) int64 {
	w := make([]int64, len(word))
	for i := 0; i < len(word); i++ {
		w[i] = int64(word[i]) - 65
	}
	const far = 1000000
	other := make([]int64, 27)
	for j := range other {
		other[j] = far
	}
	other[26] = 0
	for i := 1; i < len(w); i++ {
		last, now := w[i-1], w[i]
		next := make([]int64, 27)
		for j := range next {
			next[j] = far
		}
		for j := int64(0); j < 27; j++ {
			if other[j] < far {
				if a := other[j] + keyDistance(last, now); a < next[j] {
					next[j] = a
				}
				if b := other[j] + keyDistance(j, now); b < next[last] {
					next[last] = b
				}
			}
		}
		other = next
	}
	best := other[0]
	for _, v := range other[1:] {
		if v < best {
			best = v
		}
	}
	return best
}

var seed int64 = 1320

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	letters := []byte("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
	words := make([][]byte, 100)
	for t := 0; t < 100; t++ {
		k := int64(26)
		if t%3 == 0 {
			k = 2
		} else if t%3 == 1 {
			k = 5
		}
		base := nextRandom() % (27 - k)
		chars := make([]byte, 300)
		for i := range chars {
			chars[i] = letters[base+nextRandom()%k]
		}
		words[t] = chars
	}
	var check int64
	for pass := int64(0); pass < 80; pass++ {
		for t := 0; t < 100; t++ {
			words[t][check%300] = letters[(check/7)%26]
			got := minimumDistance(string(words[t]))
			check = (check*31 + got + pass) % 1000000007
		}
	}
	fmt.Printf("80 passes over 100 words of 300: checksum %d\n", check)
}
