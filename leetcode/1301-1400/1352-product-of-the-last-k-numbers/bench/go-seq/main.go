// LeetCode #1352 bench -- Go: the running products since the last zero,
// after a leading 1.
package main

import "fmt"

type ProductOfNumbers struct {
	prefix []int64
}

func (p *ProductOfNumbers) Add(num int32) {
	if num == 0 {
		p.prefix = append(p.prefix[:0], 1)
		return
	}
	p.prefix = append(p.prefix, p.prefix[len(p.prefix)-1]*int64(num))
}

func (p *ProductOfNumbers) GetProduct(k int64) int32 {
	n := int64(len(p.prefix))
	if k >= n {
		return 0
	}
	return int32(p.prefix[n-1] / p.prefix[n-1-k])
}

func main() {
	var seed int64 = 1352
	next := func() int64 {
		seed = (seed*1103515245 + 12345) % 2147483648
		return seed / 65536
	}
	var since int64 = 1
	p := &ProductOfNumbers{prefix: []int64{1}}
	var check int64
	for r := int64(0); r < 10000000; r++ {
		var num int64 = 1
		if next()%1000 == 0 {
			num = 0
			since = 1
		} else {
			if next()%20 == 0 {
				num = 2 + next()%99
			}
			if since*num >= 2147483648 {
				num = 1
			}
			since *= num
		}
		p.Add(int32(num))
		lim := r + 1
		if lim > 50000 {
			lim = 50000
		}
		k := 1 + check%lim
		check = (check*31 + int64(p.GetProduct(k)) + r) % 1000000007
	}
	fmt.Printf("10000000 rounds: checksum %d\n", check)
}
