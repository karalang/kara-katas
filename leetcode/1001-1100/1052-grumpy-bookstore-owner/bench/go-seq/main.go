// LeetCode #1052: Grumpy Bookstore Owner -- Go mirror of bench/grumpy.kara.
package main

import "fmt"

var seed int64 = 1052

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func maxSatisfied(customers, grumpy []int64, minutes int) int64 {
	var base, saved, best int64
	for i := range customers {
		if grumpy[i] == 0 {
			base += customers[i]
		} else {
			saved += customers[i]
		}
		if i >= minutes && grumpy[i-minutes] == 1 {
			saved -= customers[i-minutes]
		}
		if saved > best {
			best = saved
		}
	}
	return base + best
}

func main() {
	days, n, techniques := 200, int64(20000), 10
	customers := make([][]int64, days)
	grumpy := make([][]int64, days)
	for d := 0; d < days; d++ {
		customers[d] = make([]int64, n)
		grumpy[d] = make([]int64, n)
		for i := int64(0); i < n; i++ {
			customers[d][i] = nextRandom() % 1001
			grumpy[d][i] = nextRandom() % 2
		}
	}
	var total, check int64
	for d := 0; d < days; d++ {
		for t := 0; t < techniques; t++ {
			minutes := nextRandom()%n + 1
			answer := maxSatisfied(customers[d], grumpy[d], int(minutes))
			total += answer
			check = (check*131 + answer) % 1000000007
		}
	}
	fmt.Printf("%d days of %d minutes, %d techniques each: total %d, checksum %d\n", days, n, techniques, total, check)
}
