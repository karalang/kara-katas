// Benchmark harness for LeetCode #242 — Valid Anagram.
// Mirrors valid_anagram.kara algorithm-for-algorithm.
package main

import "fmt"

func isAnagram(s []byte, t []byte) bool {
	if len(s) != len(t) {
		return false
	}
	var count [26]int64
	for i := 0; i < len(s); i++ {
		count[s[i]-97]++
		count[t[i]-97]--
	}
	for j := 0; j < 26; j++ {
		if count[j] != 0 {
			return false
		}
	}
	return true
}

const (
	NP    = 8
	SL    = 20000
	Iters = 8000
)

func main() {
	esses := make([][]byte, NP)
	tees := make([][]byte, NP)
	for j := 0; j < NP; j++ {
		sj := make([]byte, SL)
		for k := 0; k < SL; k++ {
			sj[k] = byte(97 + ((k*7 + j) % 26))
		}
		tj := make([]byte, 0, SL)
		for m := SL - 1; m >= 0; m-- {
			b := int(sj[m])
			if j%2 == 1 && m == 0 {
				b = 97 + ((b - 97 + 1) % 26)
			}
			tj = append(tj, byte(b))
		}
		esses[j] = sj
		tees[j] = tj
	}

	var sink int64
	for it := 0; it < Iters; it++ {
		idx := (it * 3) % NP
		if isAnagram(esses[idx], tees[idx]) {
			sink += int64(it) + 1
		} else {
			sink++
		}
	}
	fmt.Println(sink)
}
