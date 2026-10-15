// LeetCode #683: K Empty Slots -- a window over the days. Bench.
package main

import "fmt"

var seed int64 = 683

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func kEmptySlots(bulbs []int64, k int64) int64 {
	n := int64(len(bulbs))
	days := make([]int64, n)
	for d := int64(0); d < n; d++ {
		days[bulbs[d]-1] = d + 1
	}
	best, left, right, i := int64(-1), int64(0), k+1, int64(1)
	for right < n {
		if i == right {
			day := days[left]
			if days[right] > day {
				day = days[right]
			}
			if best == -1 || day < best {
				best = day
			}
			left = right
			right = left + k + 1
			i = left + 1
		} else if days[i] < days[left] || days[i] < days[right] {
			left = i
			right = left + k + 1
			i = left + 1
		} else {
			i++
		}
	}
	return best
}

func main() {
	const count, n, rounds = 100, 20000, 30
	orders := make([][]int64, count)
	for c := range orders {
		v := make([]int64, n)
		for x := range v {
			v[x] = int64(x + 1)
		}
		for i := int64(n - 1); i > 0; i-- {
			a := nextRandom()
			j := (a*32768 + nextRandom()) % (i + 1)
			v[i], v[j] = v[j], v[i]
		}
		orders[c] = v
	}
	var sum, none int64
	for r := int64(0); r < rounds; r++ {
		for c := int64(0); c < count; c++ {
			k := (c*7 + r) % 50
			day := kEmptySlots(orders[c], k)
			if day == -1 {
				none++
			}
			sum = (sum*31 + day + 2) % 1000000007
		}
	}
	fmt.Printf("%d answers: %d without a day, checksum %d\n", count*rounds, none, sum)
}
