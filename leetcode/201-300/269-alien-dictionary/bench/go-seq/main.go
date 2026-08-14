// Benchmark workload for LeetCode #269 — Alien Dictionary (Go mirror).
// Mirrors alien.kara algorithm-for-algorithm, including the flat corpus and the
// hoisted working structures (see that file for why).
package main

import "fmt"

func main() {
	var lists int64 = 20000
	var rounds int64 = 60
	var alpha int64 = 8

	letters := []int64{}
	wstart := []int64{}
	wlen := []int64{}
	lstart := []int64{}
	lcount := []int64{}

	var state int64 = 269269
	for li := int64(0); li < lists; li++ {
		state = (state*1103515245 + 12345) & 2147483647
		m := (state/65536)%5 + 2

		rank := make([]int64, alpha)
		for z := int64(0); z < alpha; z++ {
			rank[z] = z
		}
		for sh := alpha - 1; sh > 0; sh-- {
			state = (state*1103515245 + 12345) & 2147483647
			j := (state / 65536) % (sh + 1)
			rank[sh], rank[j] = rank[j], rank[sh]
		}

		buf := []int64{}
		st := []int64{}
		ln := []int64{}
		for wi := int64(0); wi < m; wi++ {
			state = (state*1103515245 + 12345) & 2147483647
			L := (state/65536)%4 + 1
			st = append(st, int64(len(buf)))
			ln = append(ln, L)
			for p := int64(0); p < L; p++ {
				state = (state*1103515245 + 12345) & 2147483647
				buf = append(buf, (state/65536)%alpha)
			}
		}

		for a := int64(1); a < m; a++ {
			b := a
			for b > 0 {
				s1, n1 := st[b-1], ln[b-1]
				s2, n2 := st[b], ln[b]
				lim := n1
				if n2 < lim {
					lim = n2
				}
				k := int64(0)
				swap, decided := false, false
				for k < lim {
					if buf[s1+k] != buf[s2+k] {
						if rank[buf[s1+k]] > rank[buf[s2+k]] {
							swap = true
						}
						decided = true
						k = lim
					} else {
						k++
					}
				}
				if !decided && n1 > n2 {
					swap = true
				}
				if swap {
					st[b-1], st[b] = st[b], st[b-1]
					ln[b-1], ln[b] = ln[b], ln[b-1]
					b--
				} else {
					b = 0
				}
			}
		}

		state = (state*1103515245 + 12345) & 2147483647
		if (state/65536)%2 == 0 && m >= 2 {
			state = (state*1103515245 + 12345) & 2147483647
			at := (state / 65536) % (m - 1)
			st[at], st[at+1] = st[at+1], st[at]
			ln[at], ln[at+1] = ln[at+1], ln[at]
		}

		lstart = append(lstart, int64(len(wstart)))
		lcount = append(lcount, m)
		for q := int64(0); q < m; q++ {
			wstart = append(wstart, int64(len(letters)))
			wlen = append(wlen, ln[q])
			for r := int64(0); r < ln[q]; r++ {
				letters = append(letters, buf[st[q]+r])
			}
		}
	}

	adj := make([]bool, 676)
	indeg := make([]int64, 26)
	present := make([]bool, 26)
	done := make([]bool, 26)

	var sink int64 = 0
	for r0 := int64(0); r0 < rounds; r0++ {
		for idx := int64(0); idx < lists; idx++ {
			base, n := lstart[idx], lcount[idx]

			for c := 0; c < 26; c++ {
				indeg[c] = 0
				present[c] = false
				done[c] = false
			}
			for e := 0; e < 676; e++ {
				adj[e] = false
			}

			for w := int64(0); w < n; w++ {
				s, L := wstart[base+w], wlen[base+w]
				for p := int64(0); p < L; p++ {
					present[letters[s+p]] = true
				}
			}

			bad := false
			p2 := int64(0)
			for p2+1 < n {
				s1, n1 := wstart[base+p2], wlen[base+p2]
				s2, n2 := wstart[base+p2+1], wlen[base+p2+1]
				lim := n1
				if n2 < lim {
					lim = n2
				}
				k := int64(0)
				found := false
				for k < lim {
					x, y := letters[s1+k], letters[s2+k]
					if x != y {
						if !adj[x*26+y] {
							adj[x*26+y] = true
							indeg[y]++
						}
						found = true
						k = lim
					} else {
						k++
					}
				}
				if !found && n1 > n2 {
					bad = true
					p2 = n
				} else {
					p2++
				}
			}

			var acc int64 = 0
			if !bad {
				var remaining int64 = 0
				for d := 0; d < 26; d++ {
					if present[d] {
						remaining++
					}
				}
				var placed int64 = 0
				for placed < remaining {
					pick := int64(-1)
					for s3 := 0; s3 < 26; {
						if present[s3] && !done[s3] && indeg[s3] == 0 {
							pick = int64(s3)
							s3 = 26
						} else {
							s3++
						}
					}
					if pick < 0 {
						acc = 0
						placed = remaining
					} else {
						done[pick] = true
						acc = (acc*31 + pick + 1) % 1000000007
						placed++
						for t := int64(0); t < 26; t++ {
							if adj[pick*26+t] {
								indeg[t]--
							}
						}
					}
				}
			}
			sink = (sink*131 + acc) % 1000000007
		}
	}
	fmt.Println(sink)
}
