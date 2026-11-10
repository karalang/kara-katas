// LeetCode #2106: Maximum Fruits Harvested After at Most K Steps --
// bench, Go mirror of harvest.kara.
package main

import "fmt"

func steps(l, r, start int64) int64 {
	if l >= start {
		return r - start
	}
	if r <= start {
		return start - l
	}
	return min(2*(start-l)+(r-start), (start-l)+2*(r-start))
}

func maxTotalFruits(fruits [][2]int64, start, k int64) int64 {
	left := 0
	var sum, best int64
	for right := range fruits {
		sum += fruits[right][1]
		for left <= right && steps(fruits[left][0], fruits[right][0], start) > k {
			sum -= fruits[left][1]
			left++
		}
		best = max(best, sum)
	}
	return best
}

var seed int64 = 2106

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	hi := nextRandom()
	return hi*32768 + nextRandom()
}

func main() {
	fields := make([][][2]int64, 0, 20)
	for f := 0; f < 20; f++ {
		var fruits [][2]int64
		for p := int64(0); p < 200000; p++ {
			if nextRandom()%2 == 0 {
				fruits = append(fruits, [2]int64{p, wideRandom()%10000 + 1})
			}
		}
		fields = append(fields, fruits)
	}
	var total, check int64
	for _, fruits := range fields {
		for q := 0; q < 10; q++ {
			start := wideRandom() % 200001
			k := wideRandom() % 200001
			got := maxTotalFruits(fruits, start, k)
			total += got
			check = (check*31 + got) % 1000000007
		}
	}
	fmt.Printf("200 walks: %d fruits, checksum %d\n", total, check)
}
