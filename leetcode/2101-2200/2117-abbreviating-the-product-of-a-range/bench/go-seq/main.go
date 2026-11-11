// LeetCode #2117: Abbreviating the Product of a Range -- the benchmark,
// the same algorithm as abbreviate.kara: the factors of 2 and 5 pulled
// out, the rest modulo 100000 and capped at 10^11, and a float64 of the
// leading digits.

package main

import (
	"fmt"
	"strings"
)

func abbreviateProduct(left, right int64) string {
	const capped = int64(100000000000)
	var twos, fives int64
	last, exact := int64(1), int64(1)
	lead := 1.0
	for i := left; i <= right; i++ {
		x := i
		for x%2 == 0 {
			x /= 2
			twos++
		}
		for x%5 == 0 {
			x /= 5
			fives++
		}
		last = last * x % 100000
		if exact > capped/x {
			exact = capped
		} else {
			exact *= x
		}
		lead *= float64(i)
		for lead >= 1e12 {
			lead /= 10.0
		}
	}
	zeros := twos
	if fives < zeros {
		zeros = fives
	}
	for k := int64(0); k < twos-zeros; k++ {
		last = last * 2 % 100000
		if exact > capped/2 {
			exact = capped
		} else {
			exact *= 2
		}
	}
	for k := int64(0); k < fives-zeros; k++ {
		last = last * 5 % 100000
		if exact > capped/5 {
			exact = capped
		} else {
			exact *= 5
		}
	}
	if exact < 10000000000 {
		return fmt.Sprintf("%de%d", exact, zeros)
	}
	for lead >= 1e5 {
		lead /= 10.0
	}
	return fmt.Sprintf("%d...%05de%d", int64(lead), last, zeros)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(2117)
	var long, check int64
	for t := 0; t < 40000; t++ {
		left := nextRandom(&seed)%10000 + 1
		right := left + nextRandom(&seed)%3000
		if right > 10000 {
			right = 10000
		}
		got := abbreviateProduct(left, right)
		if strings.Contains(got, "...") {
			long++
		}
		for _, b := range []byte(got) {
			check = (check*31 + int64(b)) % 1000000007
		}
	}
	fmt.Printf("40000 solves: %d long answers, checksum %d\n", long, check)
}
