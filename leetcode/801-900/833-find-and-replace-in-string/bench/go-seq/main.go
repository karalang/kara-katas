// Benchmark for #833: Find And Replace in String -- the ★ arm (a table by index).
//
// Mirrors find_replace_string.kara: each operation whose source occurs at
// its index is recorded in a table at that index, and one walk over the
// string writes each recorded operation's target in place of its source
// and copies the other letters.
package main

import (
	"fmt"
	"strings"
)

func findReplaceString(s string, indices []int64, sources []string, targets []string) string {
	n := int64(len(s))
	at := make([]int64, n)
	for i := range at {
		at[i] = -1
	}
	for k := range indices {
		i := indices[k]
		if strings.HasPrefix(s[i:], sources[k]) {
			at[i] = int64(k)
		}
	}
	var out strings.Builder
	i := int64(0)
	for i < n {
		k := at[i]
		if k >= 0 {
			out.WriteString(targets[k])
			i += int64(len(sources[k]))
		} else {
			out.WriteString(s[i : i+1])
			i++
		}
	}
	return out.String()
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func letter(r int64) byte {
	return byte('a' + r)
}

type kase struct {
	s       string
	indices []int64
	sources []string
	targets []string
}

func main() {
	const count = 64
	const rounds = 300000
	const n = 1000
	seed := int64(833)
	cases := make([]kase, 0, count)
	for g := 0; g < count; g++ {
		b := make([]byte, n)
		for i := range b {
			b[i] = letter(nextRandom(&seed) % 2)
		}
		s := string(b)
		var indices []int64
		var sources, targets []string
		pos := nextRandom(&seed) % 4
		for pos < n && len(indices) < 100 {
			room := int64(10)
			if n-pos < 10 {
				room = n - pos
			}
			length := 1 + nextRandom(&seed)%room
			src := []byte(s[pos : pos+length])
			if nextRandom(&seed)%3 == 2 {
				last := int64(src[length-1]) - 97
				src[length-1] = letter((last + 1) % 26)
			}
			tlen := 1 + nextRandom(&seed)%7
			target := make([]byte, tlen)
			for t := range target {
				target[t] = letter(nextRandom(&seed) % 26)
			}
			indices = append(indices, pos)
			sources = append(sources, string(src))
			targets = append(targets, string(target))
			pos += length + nextRandom(&seed)%4
		}
		i := int64(len(indices))
		for i > 1 {
			j := nextRandom(&seed) % i
			i--
			indices[i], indices[j] = indices[j], indices[i]
			sources[i], sources[j] = sources[j], sources[i]
			targets[i], targets[j] = targets[j], targets[i]
		}
		cases = append(cases, kase{s, indices, sources, targets})
	}
	total := int64(0)
	checksum := int64(0)
	for round := int64(0); round < rounds; round++ {
		c := cases[round%count]
		out := findReplaceString(c.s, c.indices, c.sources, c.targets)
		total += int64(len(out))
		checksum = (checksum*131 + int64(out[round/count%int64(len(out))])) % 1000000007
	}
	fmt.Printf("%d rounds of %d cases: %d letters, checksum %d\n", rounds, count, total, checksum)
}
