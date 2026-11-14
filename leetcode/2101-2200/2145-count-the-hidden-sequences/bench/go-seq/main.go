// LeetCode #2145: Count the Hidden Sequences -- the benchmark, the same
// algorithm as hidden.kara.
package main

import "fmt"

func numberOfArrays(differences []int64, lower, upper int64) int64 {
	at, lowest, highest := int64(0), int64(0), int64(0)
	for _, d := range differences {
		at += d
		if at < lowest {
			lowest = at
		}
		if at > highest {
			highest = at
		}
	}
	count := (upper - lower) - (highest - lowest) + 1
	if count < 0 {
		return 0
	}
	return count
}

var seed int64 = 2145

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	walks := make([][]int64, 20)
	for w := range walks {
		walks[w] = make([]int64, 100000)
		for i := range walks[w] {
			walks[w][i] = nextRandom()%21 - 10
		}
	}
	total, check := int64(0), int64(0)
	for round := int64(0); round < 200; round++ {
		for w := 0; w < 20; w++ {
			hi := nextRandom()
			at := (hi*32768 + nextRandom()) % 100000
			walks[w][at] = nextRandom()%21 - 10
			count := numberOfArrays(walks[w], -100000, 100000)
			total += count
			check = (check*31 + count + round) % 1000000007
		}
	}
	fmt.Printf("4000 solves: %d sequences in all, checksum %d\n", total, check)
}
