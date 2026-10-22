// Benchmark for #844: Backspace String Compare -- Go twin of the Kāra ★ arm
// (two pointers from the back).
package main

import "fmt"

// the index of the last surviving character at or before `i`, or -1
func nextKept(s string, i int) int {
	skip := 0
	for i >= 0 {
		if s[i] == '#' {
			skip++
		} else if skip > 0 {
			skip--
		} else {
			return i
		}
		i--
	}
	return -1
}

func backspaceCompare(a, b string) bool {
	i := nextKept(a, len(a)-1)
	j := nextKept(b, len(b)-1)
	for i >= 0 && j >= 0 {
		if a[i] != b[j] {
			return false
		}
		i = nextKept(a, i-1)
		j = nextKept(b, j-1)
	}
	return i < 0 && j < 0
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds = 64, 3500000
	seed := int64(844)
	firsts := make([]string, 0, count)
	seconds := make([]string, 0, count)
	for g := 0; g < count; g++ {
		k := int64(2 + g%3)
		cs := []byte{}
		for i := 0; i < 120; i++ {
			if nextRandom(&seed)%10 < 3 {
				cs = append(cs, '#')
			} else {
				cs = append(cs, byte(97+nextRandom(&seed)%k))
			}
		}
		first := string(cs)
		for e := 0; e < 40; e++ {
			at := int(nextRandom(&seed) % int64(len(cs)+1))
			cs = append(cs[:at], append([]byte{'#'}, cs[at:]...)...)
			cs = append(cs[:at], append([]byte{byte(97 + nextRandom(&seed)%k)}, cs[at:]...)...)
		}
		if g%2 == 1 {
			at := nextRandom(&seed) % int64(len(cs))
			if cs[at] == '#' {
				cs[at] = 'a'
			} else {
				cs[at] = '#'
			}
		}
		firsts = append(firsts, first)
		seconds = append(seconds, string(cs))
	}
	equal, checksum := 0, int64(0)
	for round := 0; round < rounds; round++ {
		g := round % count
		same := backspaceCompare(firsts[g], seconds[g])
		if same {
			equal++
			checksum = (checksum*31 + int64(round%1000)) % 1000000007
		} else {
			checksum = (checksum*31 + 7) % 1000000007
		}
	}
	fmt.Printf("%d rounds of %d pairs: %d equal, checksum %d\n", rounds, count, equal, checksum)
}
