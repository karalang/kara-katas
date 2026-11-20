// LeetCode #1672: Richest Customer Wealth -- the bench's Go mirror: the ★
// arm on 4000 grids of 50 customers by 50 banks, up to 100 in each
// account, all drawn first, each answered 100 times.
package main

import "fmt"

func maximumWealth(accounts [][]int32) int32 {
	var richest int32
	for i, row := range accounts {
		var wealth int32
		for _, money := range row {
			wealth += money
		}
		if i == 0 || wealth > richest {
			richest = wealth
		}
	}
	return richest
}

var seed int64 = 1672

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const grids = 4000
	const side = 50
	const rounds = 100
	all := make([][][]int32, grids)
	for g := range all {
		all[g] = make([][]int32, side)
		for i := range all[g] {
			all[g][i] = make([]int32, side)
			for j := range all[g][i] {
				all[g][i][j] = int32(nextRandom()%100 + 1)
			}
		}
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, accounts := range all {
			richest := int64(maximumWealth(accounts))
			total += richest
			check = (check*31 + richest + r) % 1000000007
		}
	}
	fmt.Printf("%d grids of %d by %d, %d rounds: answers sum to %d, checksum %d\n", grids, side, side, rounds, total, check)
}
