// Benchmark for #375 -- mirror of money_amount.kara.
package main

import (
	"fmt"
	"math"
)

func getMoneyAmount(n int) int64 {
	cost := make([][]int64, n+2)
	for i := range cost {
		cost[i] = make([]int64, n+2)
	}
	for length := 2; length <= n; length++ {
		for i := 1; i <= n-length+1; i++ {
			j := i + length - 1
			best := int64(math.MaxInt64)
			for k := i; k <= j; k++ {
				worse := cost[i][k-1]
				if cost[k+1][j] > worse {
					worse = cost[k+1][j]
				}
				if int64(k)+worse < best {
					best = int64(k) + worse
				}
			}
			cost[i][j] = best
		}
	}
	return cost[1][n]
}

func main() {
	var checksum int64
	for n := 1; n <= 200; n++ {
		checksum = (checksum*1009 + getMoneyAmount(n)) % 1000000007
	}
	fmt.Printf("checksum %d\n", checksum)
}
