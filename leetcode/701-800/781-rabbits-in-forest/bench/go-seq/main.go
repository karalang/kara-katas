// Benchmark for #781: Rabbits in Forest -- mirror of the ★ arm (groups
// counted by answer), with the same workload as the Kāra program.
package main

import "fmt"

func numRabbits(answers []int64) int64 {
	count := map[int64]int64{}
	for _, a := range answers {
		count[a]++
	}
	var total int64
	for v, c := range count {
		size := v + 1
		total += (c + size - 1) / size * size
	}
	return total
}

var seed int64 = 781

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count = 64
	forests := make([][]int64, count)
	for g := 0; g < count; g++ {
		top := int64(1000)
		if g%3 == 0 {
			top = 10
		} else if g%3 == 1 {
			top = 100
		}
		forests[g] = make([]int64, 1000)
		for i := range forests[g] {
			forests[g][i] = nextRandom() % top
		}
	}
	var total, checksum int64
	for round := int64(0); round < 50000; round++ {
		g := (round * 7) % count
		rabbits := numRabbits(forests[g])
		total += rabbits
		checksum = (checksum*31 + rabbits + g) % 1000000007
	}
	fmt.Printf("50000 rounds of 1000 answers: %d rabbits, checksum %d\n", total, checksum)
}
