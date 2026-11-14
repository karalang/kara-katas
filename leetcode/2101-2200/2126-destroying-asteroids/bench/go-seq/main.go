// LeetCode #2126: Destroying Asteroids -- the benchmark, the same
// algorithm as asteroids.kara.
package main

import (
	"fmt"
	"slices"
)

func asteroidsDestroyed(mass int64, asteroids []int64) bool {
	sorted := slices.Clone(asteroids)
	slices.Sort(sorted)
	planet := mass
	for _, a := range sorted {
		if planet < a {
			return false
		}
		planet += a
	}
	return true
}

var seed int64 = 2126

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int64, 20)
	for k := range arrays {
		arrays[k] = make([]int64, 100000)
		for i := range arrays[k] {
			hi := nextRandom()
			arrays[k][i] = (hi*32768+nextRandom())%99001 + 1000
		}
	}
	var destroyed, check int64
	for round := int64(0); round < 10; round++ {
		for k := int64(0); k < 20; k++ {
			hi := nextRandom()
			at := (hi*32768 + nextRandom()) % 100000
			arrays[k][at] = nextRandom()%2000 + 1
			mass := nextRandom()%1000 + 500
			if asteroidsDestroyed(mass, arrays[k]) {
				destroyed++
				check = (check*31 + round*20 + k) % 1000000007
			}
		}
	}
	fmt.Printf("200 solves: %d destroyed, checksum %d\n", destroyed, check)
}
