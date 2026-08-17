// LeetCode 278 bench mirror — Go. Build one dictionary, solve it 48 times.
package main

import "fmt"

const Words = 250000
const Alpha = 6
const Width = 8
const Instances = 48

func solveLen(dict [][]byte) int64 {
	var present [26]bool
	var indeg [26]int64
	adj := make([]bool, 676)
	for _, w := range dict {
		for _, ch := range w {
			present[ch-'a'] = true
		}
	}
	for p := 0; p+1 < len(dict); p++ {
		a, c := dict[p], dict[p+1]
		found := false
		shorter := len(a)
		if len(c) < shorter {
			shorter = len(c)
		}
		for k := 0; k < shorter; k++ {
			if a[k] != c[k] {
				u, v := int(a[k]-'a'), int(c[k]-'a')
				if !adj[u*26+v] {
					adj[u*26+v] = true
					indeg[v]++
				}
				found = true
				break
			}
		}
		if !found && len(a) > len(c) {
			return 0
		}
	}
	var done [26]bool
	remaining := 0
	for r := 0; r < 26; r++ {
		if present[r] {
			remaining++
		}
	}
	var out int64
	for remaining > 0 {
		pick := -1
		for s := 0; s < 26; s++ {
			if present[s] && !done[s] && indeg[s] == 0 {
				pick = s
				break
			}
		}
		if pick < 0 {
			return 0
		}
		done[pick] = true
		out++
		for t := 0; t < 26; t++ {
			if adj[pick*26+t] {
				indeg[t]--
			}
		}
		remaining--
	}
	return out
}

func main() {
	dict := make([][]byte, Words)
	for n := 0; n < Words; n++ {
		rem := n
		var digits [Width]int
		for pos := 0; pos < Width; pos++ {
			digits[pos] = rem % Alpha
			rem /= Alpha
		}
		w := make([]byte, 0, Width)
		for q := Width - 1; q >= 0; q-- {
			w = append(w, byte('a'+(Alpha-1-digits[q])))
		}
		dict[n] = w
	}
	var sink int64
	for i := int64(0); i < Instances; i++ {
		sink = (sink + (i*1000003+solveLen(dict))%1000000007) % 1000000007
	}
	fmt.Println(sink)
}
