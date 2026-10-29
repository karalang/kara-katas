// LeetCode #1025: Divisor Game -- bench
// Mirrors ../divisor_game.kara; see ../../README.md § Benchmarks.

package main

import "fmt"

func divisorGame(n int64) bool {
	divisors := make([][]int64, n+1)
	for x := int64(1); x <= n/2; x++ {
		for m := 2 * x; m <= n; m += x {
			divisors[m] = append(divisors[m], x)
		}
	}
	wins := make([]bool, n+1)
	for m := int64(2); m <= n; m++ {
		for _, x := range divisors[m] {
			if !wins[m-x] {
				wins[m] = true
				break
			}
		}
	}
	return wins[n]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := 100
	rounds := 100
	seed := int64(1025)
	games := make([]int64, 0, count)
	for i := 0; i < count; i++ {
		games = append(games, 500+nextRandom(&seed)%501)
	}
	var wins, check int64
	for r := 0; r < rounds; r++ {
		for _, n := range games {
			alice := divisorGame(n)
			if alice {
				wins++
			}
			a := int64(0)
			if alice {
				a = 1
			}
			check = (check*131 + n*2 + a) % 1000000007
		}
	}
	fmt.Printf("%d games of n from 500 to 1000, %d rounds: Alice wins %d, checksum %d\n", count, rounds, wins, check)
}
