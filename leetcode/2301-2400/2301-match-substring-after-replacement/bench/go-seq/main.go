// LeetCode #2301: Match Substring After Replacement -- the bench, the ★
// arm in Go. A table of which letter may stand for which, then every
// start of sub in s checked against it.
package main

import "fmt"

func matchReplacement(s, sub string, mappings [][2]byte) bool {
	can := make([]bool, 128*128)
	for c := 0; c < 128; c++ {
		can[c*128+c] = true
	}
	for _, m := range mappings {
		can[int(m[0])*128+int(m[1])] = true
	}
	for start := 0; start <= len(s)-len(sub); start++ {
		all := true
		for j := 0; j < len(sub); j++ {
			if !can[int(sub[j])*128+int(s[start+j])] {
				all = false
				break
			}
		}
		if all {
			return true
		}
	}
	return false
}

var seed int64 = 2301

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	ab := "ab"
	xyz := "xyz"
	texts := make([]string, 0, 50)
	subs := make([]string, 0, 50)
	maps := make([][][2]byte, 0, 50)
	for c := 0; c < 50; c++ {
		s := make([]byte, 20000)
		for i := range s {
			s[i] = ab[nextRandom()%2]
		}
		sub := make([]byte, 40)
		for j := range sub {
			r := nextRandom() % 4
			if r < 2 {
				sub[j] = 'c'
			} else {
				sub[j] = ab[r-2]
			}
		}
		mappings := [][2]byte{{'c', 'a'}, {'c', 'b'}}
		for i := 0; i < 998; i++ {
			old := xyz[nextRandom()%3]
			nw := ab[nextRandom()%2]
			mappings = append(mappings, [2]byte{old, nw})
		}
		texts = append(texts, string(s))
		subs = append(subs, string(sub))
		maps = append(maps, mappings)
	}
	var check int64
	for p := 0; p < 20; p++ {
		for c := 0; c < 50; c++ {
			v := int64(0)
			if matchReplacement(texts[(c+p)%50], subs[c], maps[c]) {
				v = int64(c + 1)
			}
			check = (check*31 + v) % 1000000007
		}
	}
	fmt.Printf("20 passes over 50 cases of 20000 letters: checksum %d\n", check)
}
