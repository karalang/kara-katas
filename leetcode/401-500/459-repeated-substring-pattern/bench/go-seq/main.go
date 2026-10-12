// Benchmark for #459: mirror of repeated_substring.kara (the ★ arm, every
// proper divisor) on the same workload.
package main

import (
	"fmt"
	"strings"
)

func repeatedSubstringPattern(s string) bool {
	cs := []rune(s)
	n := len(cs)
	for d := 1; d < n/2+1; d++ {
		if n%d != 0 {
			continue
		}
		repeats := true
		for i := d; i < n; i++ {
			if cs[i] != cs[i-d] {
				repeats = false
				break
			}
		}
		if repeats {
			return true
		}
	}
	return false
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const nStrings = 10
	const n int64 = 100000
	const rounds = 40
	units := []int64{1, 5, 32, 100, 625, 1000, 3125, 5000, 20000, 50000}
	seed := int64(459)
	all := make([]string, 0, nStrings)
	for a := 0; a < nStrings; a++ {
		var unit strings.Builder
		for i := int64(0); i < units[a]; i++ {
			unit.WriteRune(rune(97 + nextRandom(&seed)%26))
		}
		all = append(all, strings.Repeat(unit.String(), int(n/units[a])))
	}
	found := 0
	checksum := int64(0)
	for r := 0; r < rounds; r++ {
		for a := 0; a < nStrings; a++ {
			hi := nextRandom(&seed)
			lo := nextRandom(&seed)
			k := n/2 + (hi*65536+lo)%(n/2)
			punch := nextRandom(&seed)%2 == 0
			original := strings.Clone(all[a])
			if punch {
				cs := []rune(all[a])
				cs[k] = rune(97 + (int64(cs[k])-97+1)%26)
				all[a] = string(cs)
			}
			has := repeatedSubstringPattern(all[a])
			all[a] = original
			if has {
				found++
			}
			v := k
			if has {
				v = units[a]
			}
			checksum = (checksum*31 + v) % 1000000007
		}
	}
	fmt.Printf("%d rounds on %d strings of %d: %d repeat a substring, checksum %d\n", rounds, nStrings, n, found, checksum)
}
