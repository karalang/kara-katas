// Benchmark for #374 -- mirror of guess_number.kara.
package main

import "fmt"

type game struct{ pick, calls int64 }

func (g *game) guess(num int64) int64 {
	g.calls++
	if g.pick < num {
		return -1
	}
	if g.pick > num {
		return 1
	}
	return 0
}

func guessNumber(n int64, g *game) int64 {
	lo, hi := int64(1), n
	for lo <= hi {
		mid := lo + (hi-lo)/2
		answer := g.guess(mid)
		if answer == 0 {
			return mid
		} else if answer < 0 {
			hi = mid - 1
		} else {
			lo = mid + 1
		}
	}
	return -1
}

func main() {
	var seed, checksum, guesses int64 = 374, 0, 0
	for round := 0; round < 2000000; round++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		high := seed / 65536
		seed = (seed*1103515245 + 12345) % 2147483648
		n := 1 + (high*65536+seed/32768)%2147483647
		seed = (seed*1103515245 + 12345) % 2147483648
		high2 := seed / 65536
		seed = (seed*1103515245 + 12345) % 2147483648
		pick := 1 + (high2*65536+seed/32768)%n
		g := game{pick, 0}
		got := guessNumber(n, &g)
		guesses += g.calls
		checksum = (checksum*31 + got) % 1000000007
	}
	fmt.Printf("%d guesses, checksum %d\n", guesses, checksum)
}
