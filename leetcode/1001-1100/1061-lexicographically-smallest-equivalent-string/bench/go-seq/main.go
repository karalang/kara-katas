// LeetCode #1061: Lexicographically Smallest Equivalent String -- the
// benchmark, the same union-find as lexi.kara.
package main

import (
	"fmt"
	"strings"
)

func find(parent *[26]int64, x int64) int64 {
	root := x
	for parent[root] != root {
		root = parent[root]
	}
	y := x
	for parent[y] != root {
		next := parent[y]
		parent[y] = root
		y = next
	}
	return root
}

func smallestEquivalent(s1, s2, base string) string {
	var parent [26]int64
	for i := range parent {
		parent[i] = int64(i)
	}
	for i := 0; i < len(s1) && i < len(s2); i++ {
		ra := find(&parent, int64(s1[i]-'a'))
		rb := find(&parent, int64(s2[i]-'a'))
		if ra < rb {
			parent[rb] = ra
		} else {
			parent[ra] = rb
		}
	}
	var out strings.Builder
	for i := 0; i < len(base); i++ {
		root := find(&parent, int64(base[i]-'a'))
		out.WriteByte(byte('a' + root))
	}
	return out.String()
}

var seed int64 = 1061

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord(n, k int64) string {
	b := make([]byte, 0, n)
	for i := int64(0); i < n; i++ {
		b = append(b, byte('a'+nextRandom()%k))
	}
	return string(b)
}

func main() {
	var s1s, s2s, bases []string
	for p := int64(0); p < 100; p++ {
		k := 2 + p%25
		s1s = append(s1s, randomWord(1000, k))
		s2s = append(s2s, randomWord(1000, k))
	}
	for b := 0; b < 100; b++ {
		bases = append(bases, randomWord(20000, 26))
	}
	var calls, total, check int64
	for p := 0; p < 100; p++ {
		for b := 0; b < 100; b++ {
			answer := smallestEquivalent(s1s[p], s2s[p], bases[b])
			var sum int64
			for i := 0; i < len(answer); i++ {
				sum += int64(answer[i])
			}
			total += sum
			check = (check*31 + sum%1000003) % 1000000007
			calls++
		}
	}
	fmt.Printf("%d calls: letters sum %d, checksum %d\n", calls, total, check)
}
