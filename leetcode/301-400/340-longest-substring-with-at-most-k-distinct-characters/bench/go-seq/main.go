// Benchmark mirror of longest_k_distinct.kara (LeetCode #340): a sliding
// window with a count per character in a map. Same strings, rounds and sink.
package main

import "fmt"

func longestKDistinct(s string, k int64) int64 {
	cs := []rune(s)
	counts := map[rune]int64{}
	left := 0
	var best int64
	for right := 0; right < len(cs); right++ {
		counts[cs[right]]++
		for int64(len(counts)) > k {
			d := cs[left]
			n := counts[d] - 1
			if n == 0 {
				delete(counts, d)
			} else {
				counts[d] = n
			}
			left++
		}
		if w := int64(right - left + 1); w > best {
			best = w
		}
	}
	return best
}

func next(state *int64) int64 {
	*state = (*state*1103515245 + 12345) % 2147483648
	return *state >> 8
}

func genText(seed, n, alpha int64) string {
	letters := []rune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
	state := seed
	out := make([]rune, 0, n)
	for i := int64(0); i < n; i++ {
		out = append(out, letters[next(&state)%alpha])
	}
	return string(out)
}

func main() {
	alphas := []int64{4, 8, 12, 20, 26, 34, 44, 52}
	texts := make([]string, 8)
	for i := 0; i < 8; i++ {
		texts[i] = genText(1000+int64(i), 20000, alphas[i])
	}
	var h int64
	for r := int64(0); r < 400; r++ {
		k := (r*7)%30 + 1
		h = (h*31 + longestKDistinct(texts[r%8], k)) % 1000000007
	}
	fmt.Println(h)
}
