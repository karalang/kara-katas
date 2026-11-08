// LeetCode #1520: Maximum Number of Non-Overlapping Substrings -- the
// bench in Go: the ★ arm over 200000 random strings of 1 to 64 letters
// over 5, built once and answered 3 times.
package main

import "fmt"

func maxNumOfSubstrings(s string) []string {
	bytes := []byte(s)
	n := int64(len(bytes))
	first := make([]int64, 26)
	last := make([]int64, 26)
	for c := range first {
		first[c] = n
		last[c] = -1
	}
	for i := int64(0); i < n; i++ {
		c := bytes[i] - 97
		if i < first[c] {
			first[c] = i
		}
		last[c] = i
	}
	type span struct{ a, b int64 }
	spans := []span{}
	right := int64(-1)
	for i := int64(0); i < n; i++ {
		c := bytes[i] - 97
		if i != first[c] {
			continue
		}
		end := last[c]
		ok := true
		for j := i; j <= end; j++ {
			d := bytes[j] - 97
			if first[d] < i {
				ok = false
				break
			}
			if last[d] > end {
				end = last[d]
			}
		}
		if !ok {
			continue
		}
		if i > right {
			spans = append(spans, span{i, end})
		} else {
			spans[len(spans)-1] = span{i, end}
		}
		right = end
	}
	out := make([]string, 0, len(spans))
	for _, p := range spans {
		out = append(out, string([]byte(s[p.a:p.b+1])))
	}
	return out
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func mix(check, x int64) int64 {
	return (check*31 + x + 1) % 1000000007
}

func main() {
	const count = 200000
	seed := int64(1520)
	strings := make([]string, 0, count)
	for k := 0; k < count; k++ {
		n := nextRandom(&seed)%64 + 1
		b := make([]byte, n)
		for i := range b {
			b[i] = byte(97 + nextRandom(&seed)%5)
		}
		strings = append(strings, string(b))
	}
	check, pieces := int64(0), int64(0)
	for pass := 0; pass < 3; pass++ {
		for _, s := range strings {
			for _, piece := range maxNumOfSubstrings(s) {
				pieces++
				check = mix(check, int64(len(piece)))
				check = mix(check, int64(piece[0]))
			}
		}
	}
	fmt.Printf("3 passes over 200000 strings of up to 64 letters: %d substrings, checksum %d\n", pieces, check)
}
