// LeetCode #879 bench: Go mirror of profitable_schemes.kara (the ★ arm, a
// knapsack over members and profit) on the same 600 cases.
package main

import "fmt"

func profitableSchemes(n, minProfit int64, group, profit []int64) int64 {
	const modulus = 1000000007
	ways := make([][]int64, n+1)
	for m := range ways {
		ways[m] = make([]int64, minProfit+1)
	}
	ways[0][0] = 1
	for c := range group {
		g := group[c]
		gain := profit[c]
		for m := n; m >= g; m-- {
			for p := int64(0); p <= minProfit; p++ {
				q := min(p+gain, minProfit)
				ways[m][q] = (ways[m][q] + ways[m-g][p]) % modulus
			}
		}
	}
	var total int64
	for m := int64(0); m <= n; m++ {
		total = (total + ways[m][minProfit]) % modulus
	}
	return total
}

var seed int64 = 879

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var total, check int64
	for k := 0; k < 600; k++ {
		n := 50 + nextRandom()%51
		minProfit := 50 + nextRandom()%51
		wide := k%2 == 0
		group := make([]int64, 0, 100)
		profit := make([]int64, 0, 100)
		for c := 0; c < 100; c++ {
			if wide {
				group = append(group, nextRandom()%100+1)
				profit = append(profit, nextRandom()%101)
			} else {
				group = append(group, nextRandom()%10+1)
				profit = append(profit, nextRandom()%11)
			}
		}
		answer := profitableSchemes(n, minProfit, group, profit)
		total += answer
		check = (check*131 + answer) % 1000000007
	}
	fmt.Printf("600 cases of 100 crimes: counts sum to %d, checksum %d\n", total, check)
}
