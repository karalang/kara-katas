// Benchmark: LeetCode #970 Powerful Integers -- the ★ arm, every pair of
// powers in a set, for every x and y from 1 to 100 with bound 10^6.
// Mirrors powerful_integers.kara, .c, .rs and .py.
package main

import "fmt"

func powers(base, bound int64) []int64 {
	var out []int64
	for p := int64(1); p <= bound; p *= base {
		out = append(out, p)
		if base == 1 {
			break
		}
	}
	return out
}

func powerfulIntegers(x, y, bound int64) []int64 {
	seen := map[int64]struct{}{}
	for _, a := range powers(x, bound) {
		for _, b := range powers(y, bound-a) {
			seen[a+b] = struct{}{}
		}
	}
	out := make([]int64, 0, len(seen))
	for v := range seen {
		out = append(out, v)
	}
	return out
}

func main() {
	rounds := int64(100)
	found, check := int64(0), int64(0)
	for r := int64(0); r < rounds; r++ {
		for x := int64(1); x <= 100; x++ {
			for y := int64(1); y <= 100; y++ {
				for _, v := range powerfulIntegers(x, y, 1000000-r) {
					found++
					check = (check + v*v) % 1000000007
				}
			}
		}
	}
	fmt.Printf("%d rounds over x and y from 1 to 100: %d powerful integers, checksum %d\n", rounds, found, check)
}
