// LeetCode #2383: Minimum Hours of Training to Win a Competition -- the
// bench, the ★ arm in Go: the energy trained to one above the opponents'
// sum, the experience walked through the opponents.
package main

import "fmt"

func minNumberOfHours(initialEnergy, initialExperience int64, energy, experience []int64) int64 {
	needed := int64(1)
	for _, e := range energy {
		needed += e
	}
	hours := int64(0)
	if initialEnergy < needed {
		hours = needed - initialEnergy
	}
	have := initialExperience
	for _, e := range experience {
		if have <= e {
			hours += e + 1 - have
			have = e + 1
		}
		have += e
	}
	return hours
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 1000 contests of 100 opponents, contest c's from 1 to 1 + c % 100;
	// pass p starts contest c with (p + c) % 50 more energy and
	// (3 p + c) % 50 more experience than its own start
	seed := int64(2383)
	energies := make([][]int64, 1000)
	experiences := make([][]int64, 1000)
	starts := make([][2]int64, 1000)
	for c := int64(0); c < 1000; c++ {
		top := 1 + c%100
		starts[c][0] = 1 + nextRandom(&seed)%100
		starts[c][1] = 1 + nextRandom(&seed)%100
		energies[c] = make([]int64, 100)
		for i := range energies[c] {
			energies[c][i] = 1 + nextRandom(&seed)%top
		}
		experiences[c] = make([]int64, 100)
		for i := range experiences[c] {
			experiences[c][i] = 1 + nextRandom(&seed)%top
		}
	}
	check := int64(0)
	for p := int64(0); p < 5000; p++ {
		for c := int64(0); c < 1000; c++ {
			hours := minNumberOfHours(starts[c][0]+(p+c)%50, starts[c][1]+(3*p+c)%50, energies[c], experiences[c])
			check = (check*31 + hours + p) % 1000000007
		}
	}
	fmt.Printf("5000 passes over 1000 contests of 100 opponents: checksum %d\n", check)
}
