// LeetCode #1357 bench -- Go: the prices in a map from product to price,
// and a count of the customers so far.
package main

import (
	"fmt"
	"math"
)

type cashier struct {
	n, discount, served int32
	price               map[int32]int32
}

func newCashier(n, discount int32, products, prices []int32) *cashier {
	price := make(map[int32]int32)
	for i := range products {
		price[products[i]] = prices[i]
	}
	return &cashier{n: n, discount: discount, price: price}
}

func (c *cashier) getBill(product, amount []int32) float64 {
	c.served++
	bill := 0.0
	for i := range product {
		bill += float64(c.price[product[i]] * amount[i])
	}
	if c.served%c.n == 0 {
		return bill * float64(100-c.discount) / 100.0
	}
	return bill
}

var seed int64 = 1357

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func cents(bill float64) int64 {
	return int64(math.Round(bill * 100.0))
}

func main() {
	// 20 cashiers, each selling the products 1 to 200 at prices from 1 to
	// 1000, with n from 1 to 10 and a discount from 0 to 100, built once;
	// then 10^6 bills, each of 1 to 20 products bought 1 to 1000 times,
	// all drawn from the checksum so far, every bill folded into it in cents
	cashiers := make([]*cashier, 20)
	lists := make([][]int32, 20)
	for k := 0; k < 20; k++ {
		products := make([]int32, 200)
		for i := range products {
			products[i] = int32(i + 1)
		}
		for i := int64(0); i < 200; i++ {
			j := i + nextRandom()%(200-i)
			products[i], products[j] = products[j], products[i]
		}
		prices := make([]int32, 200)
		for i := range prices {
			prices[i] = int32(1 + nextRandom()%1000)
		}
		n := int32(1 + nextRandom()%10)
		discount := int32(nextRandom() % 101)
		cashiers[k] = newCashier(n, discount, products, prices)
		lists[k] = products
	}
	var check int64
	product := make([]int32, 0, 20)
	amount := make([]int32, 0, 20)
	for r := int64(0); r < 1000000; r++ {
		k := check % 20
		m := 1 + (check/20)%20
		product = product[:0]
		amount = amount[:0]
		for j := int64(0); j < m; j++ {
			product = append(product, lists[k][(check/7+j*37)%200])
			amount = append(amount, int32(1+(check+j)%1000))
		}
		check = (check*31 + cents(cashiers[k].getBill(product, amount)) + r) % 1000000007
	}
	fmt.Printf("1000000 bills over 20 cashiers: checksum %d\n", check)
}
