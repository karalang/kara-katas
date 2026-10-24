// Benchmark: LeetCode #943 Find the Shortest Superstring -- the ★ arm,
// the most letters saved, on sets of 12 words of 20 letters, LeetCode's
// largest. Mirrors shortest_superstring.kara, .c, .rs and .py.
package main

import "fmt"

func overlap(a, b string) int64 {
	k := int64(min(len(a), len(b))) - 1
	for k > 0 {
		if a[int64(len(a))-k:] == b[:k] {
			return k
		}
		k--
	}
	return 0
}

func shortestSuperstring(words []string) string {
	n := len(words)
	ov := make([]int64, n*n)
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			if i != j {
				ov[i*n+j] = overlap(words[i], words[j])
			}
		}
	}
	full := (1 << n) - 1
	saved := make([]int64, (full+1)*n)
	before := make([]int64, (full+1)*n)
	for s := range saved {
		saved[s] = -1
		before[s] = -1
	}
	for mask := 1; mask <= full; mask++ {
		for last := 0; last < n; last++ {
			if (mask>>last)&1 == 1 {
				rest := mask ^ (1 << last)
				if rest == 0 {
					saved[mask*n+last] = 0
				} else {
					for p := 0; p < n; p++ {
						if (rest>>p)&1 == 1 {
							s := saved[rest*n+p] + ov[p*n+last]
							if s > saved[mask*n+last] {
								saved[mask*n+last] = s
								before[mask*n+last] = int64(p)
							}
						}
					}
				}
			}
		}
	}
	last := int64(0)
	for w := 1; w < n; w++ {
		if saved[full*n+w] > saved[full*n+int(last)] {
			last = int64(w)
		}
	}
	order := make([]int, 0)
	mask := full
	for last >= 0 {
		l := int(last)
		order = append(order, l)
		p := before[mask*n+l]
		mask ^= 1 << l
		last = p
	}
	out := words[order[len(order)-1]]
	for i := len(order) - 1; i > 0; i-- {
		a, b := order[i], order[i-1]
		out = out + words[b][ov[a*n+b]:]
	}
	return out
}

var seed int64 = 943

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds, count, size, length := 10, 40, 12, 20
	sets := make([][]string, 0, count)
	for c := 0; c < count; c++ {
		letters := 2 + nextRandom()%3
		words := make([]string, 0, size)
		for len(words) < size {
			b := make([]byte, length)
			for k := range b {
				b[k] = byte(nextRandom()%letters + 97)
			}
			w := string(b)
			dup := false
			for _, h := range words {
				if h == w {
					dup = true
				}
			}
			if !dup {
				words = append(words, w)
			}
		}
		sets = append(sets, words)
	}
	total := 0
	var check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			s := shortestSuperstring(sets[(r+i)%count])
			total += len(s)
			for k := 0; k < len(s); k++ {
				check = (check*31 + int64(s[k])) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds over %d sets of %d words of %d letters: lengths adding to %d, checksum %d\n", rounds, count, size, length, total, check)
}
