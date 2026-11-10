// LeetCode #2079: Watering Plants -- Go mirror of the ★ arm's benchmark
// (water.kara): 2000 gardens of 1000 plants built first, then every
// garden answered for 500 cans, from 1000 up by 97 a can.
package main

import "fmt"

var seed int64 = 2079

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wateringPlants(plants []int64, capacity int64) int64 {
	var steps int64
	can := capacity
	for i, need := range plants {
		if can < need {
			steps += 2 * int64(i)
			can = capacity
		}
		steps++
		can -= need
	}
	return steps
}

func main() {
	gardens := make([][]int64, 2000)
	for g := range gardens {
		plants := make([]int64, 1000)
		for i := range plants {
			plants[i] = nextRandom()%1000 + 1
		}
		gardens[g] = plants
	}
	var total, check int64
	for _, plants := range gardens {
		for k := int64(0); k < 500; k++ {
			a := wateringPlants(plants, 1000+97*k)
			total += a
			check = (check*31 + a) % 1000000007
		}
	}
	fmt.Printf("1000000 answers: sum %d, checksum %d\n", total, check)
}
