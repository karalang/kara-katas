// LeetCode #2214: Minimum Health to Beat Game -- bench mirror of
// health.kara: the damage summed in one pass with its largest, then the
// sum less what the armor saves on the largest, plus 1.
package main

import "fmt"

func minimumHealth(damage []int64, armor int64) int64 {
	var total, worst int64
	for _, d := range damage {
		total += d
		worst = max(worst, d)
	}
	return total - min(worst, armor) + 1
}

var seed int64 = 2214

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

// a draw of 30 bits, since one draw stops at 32767
func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	var games [][]int64
	for g := 0; g < 100; g++ {
		// 10^5 levels, the damage up to 10, 1000 and 10^5 in turn
		top := []int64{10, 1000, 100000}[g%3]
		damage := make([]int64, 100000)
		for i := range damage {
			damage[i] = wideRandom() % (top + 1)
		}
		games = append(games, damage)
	}
	var check int64
	for _, damage := range games {
		for a := int64(0); a < 20; a++ {
			// punch: one level hurts a little more before each answer
			damage[a*4999]++
			check = (check*31 + minimumHealth(damage, a*5000)) % 1000000007
		}
	}
	fmt.Printf("100 games of 10^5, 20 armors: checksum %d\n", check)
}
