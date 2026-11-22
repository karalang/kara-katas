// LeetCode #2739: Total Distance Traveled -- the bench (distance.kara in
// Go): (m - 1) / 4 transfers, as many as the additional tank holds.
package main

import "fmt"

func distanceTraveled(mainTank, additionalTank int64) int64 {
	transfers := min((mainTank-1)/4, additionalTank)
	return (mainTank + transfers) * 10
}

var seed int64 = 2739

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count, rounds = 1000000, 100
	type pair struct{ m, a int64 }
	tanks := make([]pair, 0, count)
	for i := 0; i < count; i++ {
		m := nextRandom()%100 + 1
		a := nextRandom()%100 + 1
		tanks = append(tanks, pair{m, a})
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, t := range tanks {
			d := distanceTraveled(t.m, t.a)
			sum += d
			check = (check*31 + d + r) % 1000000007
		}
	}
	fmt.Printf("%d pairs of tanks, %d rounds: distances sum to %d, checksum %d\n", count, rounds, sum, check)
}
