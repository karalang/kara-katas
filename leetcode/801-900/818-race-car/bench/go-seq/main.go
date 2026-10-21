// Benchmark for #818: Race Car -- the ★ arm (the best run to each distance).
//
// Mirrors racecar.kara: one table of the best run to every distance up to
// the target, each entry the better of overshooting and stopping short.
package main

import "fmt"

func racecar(target int64) int64 {
	best := make([]int64, target+1)
	for t := int64(1); t <= target; t++ {
		n := int64(0)
		for (int64(1) << n) <= t {
			n++
		}
		full := (int64(1) << n) - 1
		if t == full {
			best[t] = n
			continue
		}
		shortest := n + 1 + best[full-t]
		short := (int64(1) << (n - 1)) - 1
		for m := int64(0); m < n-1; m++ {
			back := (int64(1) << m) - 1
			steps := (n - 1) + 1 + m + 1 + best[t-short+back]
			if steps < shortest {
				shortest = steps
			}
		}
		best[t] = shortest
	}
	return best[target]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	rounds := int64(40000)
	seed := int64(818)
	total := int64(0)
	checksum := int64(0)
	for r := int64(0); r < rounds; r++ {
		t := 1 + nextRandom(&seed)%10000
		answer := racecar(t)
		total += answer
		checksum = (checksum*131 + answer) % 1000000007
	}
	fmt.Printf("%d rounds of targets up to 10000: total %d, checksum %d\n", rounds, total, checksum)
}
