// LeetCode #2312: Selling Pieces of Wood -- the bench, the ★ arm in Go.
// Bottom up over every size: each piece its own price or the most of
// any one cut across it.
package main

import "fmt"

type price struct{ h, w, price int64 }

func sellingWood(m, n int64, prices []price) int64 {
	best := make([][]int64, m+1)
	for h := range best {
		best[h] = make([]int64, n+1)
	}
	for _, p := range prices {
		best[p.h][p.w] = p.price
	}
	for h := int64(1); h <= m; h++ {
		for w := int64(1); w <= n; w++ {
			for i := int64(1); i < h; i++ {
				best[h][w] = max(best[h][w], best[i][w]+best[h-i][w])
			}
			for j := int64(1); j < w; j++ {
				best[h][w] = max(best[h][w], best[h][j]+best[h][w-j])
			}
		}
	}
	return best[m][n]
}

var seed int64 = 2312

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][]price, 0, 10)
	for a := 0; a < 10; a++ {
		used := make([]bool, 200*200)
		var prices []price
		for k := 0; k < 2000; k++ {
			h := nextRandom()%200 + 1
			w := nextRandom()%200 + 1
			p := nextRandom()%1000000 + 1
			if !used[(h-1)*200+w-1] {
				used[(h-1)*200+w-1] = true
				prices = append(prices, price{h, w, p})
			}
		}
		lists = append(lists, prices)
	}
	var check int64
	for p := int64(0); p < 2; p++ {
		for a := 0; a < 10; a++ {
			prices := make([]price, len(lists[a]))
			for k, q := range lists[a] {
				prices[k] = price{q.h, q.w, q.price + p}
			}
			check = (check*31 + sellingWood(200, 200, prices)) % 1000000007
		}
	}
	fmt.Printf("2 passes over 10 lists of 2000 prices on 200 by 200: checksum %d\n", check)
}
