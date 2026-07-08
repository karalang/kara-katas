// Benchmark workload — Text Justification (LeetCode #68).
// Go single-threaded mirror of bench/text_justification.{kara,rs,c}. The ★'s
// greedy-pack + even-spread logic streaming emitted bytes (word chars + gap
// spaces) into a rolling polynomial hash — no per-call allocation. Fixed 40-word
// list, justified K=300_000 times at a swept width. See ../README.md § Benchmarks.

package main

import "fmt"

var words = []string{
	"the", "quick", "brown", "fox", "jumps", "over", "a", "lazy", "dog", "while", "gentle",
	"breeze", "carries", "autumn", "leaves", "across", "quiet", "meadow", "near", "old",
	"stone", "bridge", "where", "children", "often", "gather", "to", "watch", "river", "flow",
	"beneath", "ancient", "willow", "trees", "and", "listen", "as", "the", "wind", "hums",
}

const mod int64 = 1000000007

func justifyHash(maxWidth, h int64) int64 {
	n := int64(len(words))
	i := int64(0)
	for i < n {
		j := i
		var lineChars, count int64 = 0, 0
		for j < n {
			wl := int64(len(words[j]))
			if lineChars+wl+count <= maxWidth {
				lineChars += wl
				count++
				j++
			} else {
				break
			}
		}
		gaps := count - 1
		total := maxWidth - lineChars
		isLast := j == n

		if isLast || count == 1 {
			var used int64 = 0
			for g := int64(0); g < count; g++ {
				for _, b := range []byte(words[i+g]) {
					h = (h*131 + int64(b)) % mod
					used++
				}
				if g < count-1 {
					h = (h*131 + 32) % mod
					used++
				}
			}
			for used < maxWidth {
				h = (h*131 + 32) % mod
				used++
			}
		} else {
			base := total / gaps
			extra := total % gaps
			for g := int64(0); g < count; g++ {
				for _, b := range []byte(words[i+g]) {
					h = (h*131 + int64(b)) % mod
				}
				if g < gaps {
					sp := base
					if g < extra {
						sp++
					}
					for s := int64(0); s < sp; s++ {
						h = (h*131 + 32) % mod
					}
				}
			}
		}
		i = j
	}
	return h
}

func main() {
	const total int64 = 300000
	const span int64 = 40

	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		width := 10 + (k % span)
		acc = justifyHash(width, acc)
	}
	fmt.Println(acc)
}
