// Benchmark for #816: Ambiguous Coordinates -- mirror of the ★ arm (every
// split and every point), with the same workload as
// ambiguous_coordinates.kara.
package main

import (
	"fmt"
	"strings"
)

func ambiguousCoordinates(s string) []string {
	digits := s[1 : len(s)-1]
	out := []string{}
	for cut := 1; cut < len(digits); cut++ {
		lefts := numbers(digits[:cut])
		rights := numbers(digits[cut:])
		for _, x := range lefts {
			for _, y := range rights {
				out = append(out, fmt.Sprintf("(%s, %s)", x, y))
			}
		}
	}
	return out
}

func numbers(part string) []string {
	found := []string{}
	for point := 1; point <= len(part); point++ {
		whole := part[:point]
		fraction := part[point:]
		if (whole == "0" || !strings.HasPrefix(whole, "0")) && !strings.HasSuffix(fraction, "0") {
			if fraction == "" {
				found = append(found, whole)
			} else {
				found = append(found, fmt.Sprintf("%s.%s", whole, fraction))
			}
		}
	}
	return found
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count = 64
	const rounds int64 = 400000
	seed := int64(816)
	strs := make([][]int64, count)
	for g := 0; g < count; g++ {
		digits := make([]int64, 10)
		for k := 0; k < 10; k++ {
			if nextRandom(&seed)%4 == 0 {
				digits[k] = 0
			} else {
				digits[k] = nextRandom(&seed) % 10
			}
		}
		strs[g] = digits
	}
	total, checksum := int64(0), int64(0)
	for round := int64(0); round < rounds; round++ {
		g := round % count
		at := nextRandom(&seed) % 10
		if nextRandom(&seed)%4 == 0 {
			strs[g][at] = 0
		} else {
			strs[g][at] = nextRandom(&seed) % 10
		}
		s := "("
		for _, d := range strs[g] {
			s += fmt.Sprintf("%d", d)
		}
		s += ")"
		answer := ambiguousCoordinates(s)
		total += int64(len(answer))
		for _, c := range answer {
			checksum = (checksum*131 + int64(len(c))) % 1000000007
		}
	}
	fmt.Printf("%d rounds of 10 digits: %d coordinates, checksum %d\n", rounds, total, checksum)
}
