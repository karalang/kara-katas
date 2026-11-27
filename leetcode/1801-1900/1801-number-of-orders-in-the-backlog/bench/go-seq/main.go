// LeetCode #1801: Number of Orders in the Backlog -- the bench in Go: the ★
// arm over 400 random lists of 500 orders built once, 10000 calls.
package main

import (
	"container/heap"
	"fmt"
)

type order struct {
	price  int32
	amount int64
}

// a heap of (price, amount) pairs: max gives the largest first, else the
// smallest, comparing the price and then the amount
type book struct {
	items []order
	max   bool
}

func (b book) Len() int { return len(b.items) }
func (b book) Less(i, j int) bool {
	x, y := b.items[i], b.items[j]
	if b.max {
		return x.price > y.price || (x.price == y.price && x.amount > y.amount)
	}
	return x.price < y.price || (x.price == y.price && x.amount < y.amount)
}
func (b book) Swap(i, j int)       { b.items[i], b.items[j] = b.items[j], b.items[i] }
func (b *book) Push(x interface{}) { b.items = append(b.items, x.(order)) }
func (b *book) Pop() interface{} {
	n := len(b.items)
	x := b.items[n-1]
	b.items = b.items[:n-1]
	return x
}

func getNumberOfBacklogOrders(orders [][3]int32) int32 {
	buys := &book{max: true}
	sells := &book{}
	for _, o := range orders {
		price := o[0]
		amount := int64(o[1])
		if o[2] == 0 {
			for amount > 0 && sells.Len() > 0 && sells.items[0].price <= price {
				s := heap.Pop(sells).(order)
				if s.amount > amount {
					heap.Push(sells, order{s.price, s.amount - amount})
					amount = 0
				} else {
					amount -= s.amount
				}
			}
			if amount > 0 {
				heap.Push(buys, order{price, amount})
			}
		} else {
			for amount > 0 && buys.Len() > 0 && buys.items[0].price >= price {
				b := heap.Pop(buys).(order)
				if b.amount > amount {
					heap.Push(buys, order{b.price, b.amount - amount})
					amount = 0
				} else {
					amount -= b.amount
				}
			}
			if amount > 0 {
				heap.Push(sells, order{price, amount})
			}
		}
	}
	var total int64
	for _, x := range buys.items {
		total += x.amount
	}
	for _, x := range sells.items {
		total += x.amount
	}
	return int32(total % 1000000007)
}

var seed int64 = 1801

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][][3]int32, 400)
	for l := range lists {
		lists[l] = make([][3]int32, 500)
		for x := range lists[l] {
			lists[l][x][0] = int32(1 + nextRandom()%1000)
			lists[l][x][1] = int32(1 + nextRandom()%1000)
			lists[l][x][2] = int32(nextRandom() % 2)
		}
	}
	var check int64
	for call := int64(0); call < 10000; call++ {
		check = (check*31 + int64(getNumberOfBacklogOrders(lists[(check+call)%400]))) % 1000000007
	}
	fmt.Printf("10000 calls over 400 lists of 500 orders: checksum %d\n", check)
}
