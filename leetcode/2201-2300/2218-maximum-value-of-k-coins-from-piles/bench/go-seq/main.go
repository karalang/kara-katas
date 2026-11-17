// LeetCode #2218: Maximum Value of K Coins From Piles -- bench mirror of
// coins.kara: a knapsack over the piles, best[j] the most j coins are
// worth so far, each pile tried at every count of its top coins with j
// running down.
package main

import "fmt"

func maxValueOfCoins(piles [][]int64, k int) int64 {
	best := make([]int64, k+1)
	for _, pile := range piles {
		prefix := []int64{0}
		for _, coin := range pile {
			prefix = append(prefix, prefix[len(prefix)-1]+coin)
		}
		for j := k; j >= 1; j-- {
			most := len(pile)
			if j < most {
				most = j
			}
			for t := 1; t <= most; t++ {
				if v := best[j-t] + prefix[t]; v > best[j] {
					best[j] = v
				}
			}
		}
	}
	return best[k]
}

var seed int64 = 2218

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
	var chests [][][]int64
	for a := 0; a < 20; a++ {
		// 100 piles of 10 coins worth up to 10^5
		var piles [][]int64
		for i := 0; i < 100; i++ {
			pile := make([]int64, 10)
			for t := range pile {
				pile[t] = wideRandom()%100000 + 1
			}
			piles = append(piles, pile)
		}
		chests = append(chests, piles)
	}
	var check int64
	for a := 0; a < 20; a++ {
		for r := 0; r < 4; r++ {
			// punch: one coin is drawn again before each answer
			chests[a][r*31%100][r] = wideRandom()%100000 + 1
			check = (check*31 + maxValueOfCoins(chests[a], 600)) % 1000000007
		}
	}
	fmt.Printf("20 sets of 100 piles of 10, k = 600, 4 punches: checksum %d\n", check)
}
