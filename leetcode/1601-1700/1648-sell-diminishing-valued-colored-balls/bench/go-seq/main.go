// LeetCode #1648: Sell Diminishing-Valued Colored Balls -- the bench's Go
// mirror: the ★ arm on 100 random inventories of 100000 colors with up to
// 10^9 balls each, and an order for up to 10^9 of them, all drawn first.
package main

import (
	"fmt"
	"sort"
)

const mod = 1_000_000_007

func maxProfit(inventory []int32, orders32 int32) int32 {
	counts := make([]int64, len(inventory), len(inventory)+1)
	for i, b := range inventory {
		counts[i] = int64(b)
	}
	sort.Slice(counts, func(i, j int) bool { return counts[i] > counts[j] })
	counts = append(counts, 0)
	orders := int64(orders32)
	var profit int64
	for i := 0; i < len(counts)-1; i++ {
		width := int64(i + 1)
		high, low := counts[i], counts[i+1]
		if high == low {
			continue
		}
		series := func(stop int64) int64 { return (high + stop + 1) * (high - stop) / 2 % mod * width % mod }
		if width*(high-low) < orders {
			profit = (profit + series(low)) % mod
			orders -= width * (high - low)
		} else {
			rows := orders / width
			rest := orders % width
			profit = (profit + series(high-rows)) % mod
			profit = (profit + rest*(high-rows)%mod) % mod
			return int32(profit)
		}
	}
	return int32(profit)
}

var seed int64 = 1648

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	type item struct {
		inventory []int32
		orders    int32
	}
	cases := make([]item, 0, 100)
	for c := 0; c < 100; c++ {
		inventory := make([]int32, 100000)
		for i := range inventory {
			a := nextRandom()
			b := nextRandom()
			inventory[i] = int32((a*32768+b)%1000000000 + 1)
		}
		a := nextRandom()
		b := nextRandom()
		cases = append(cases, item{inventory, int32((a*32768+b)%1000000000 + 1)})
	}
	var check, total int64
	for _, c := range cases {
		profit := int64(maxProfit(c.inventory, c.orders))
		total += profit
		check = (check*31 + profit + 1) % 1000000007
	}
	fmt.Printf("100 inventories of 100000 colors: profits sum to %d, checksum %d\n", total, check)
}
