// LeetCode #923: 3Sum With Multiplicity -- bench: counting the values.
// Mirrors three_sum_multi.kara.
package main

import "fmt"

func threeSumMulti(arr []int64, target int64) int64 {
	const modulus = 1000000007
	var count [101]int64
	for _, v := range arr {
		count[v]++
	}
	var total int64
	for x := int64(0); x < 101; x++ {
		if 3*x > target {
			break
		}
		for y := x; y < 101; y++ {
			z := target - x - y
			if z < y {
				break
			}
			if z > 100 {
				continue
			}
			var ways int64
			if x == y && y == z {
				ways = count[x] * (count[x] - 1) * (count[x] - 2) / 6
			} else if x == y {
				ways = count[x] * (count[x] - 1) / 2 * count[z]
			} else if y == z {
				ways = count[x] * count[y] * (count[y] - 1) / 2
			} else {
				ways = count[x] * count[y] * count[z]
			}
			total = (total + ways) % modulus
		}
	}
	return total
}

var seed int64 = 923

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const rounds, count, n = 500, 100, 3000
	// count arrays of n values from 0 to 100, built once
	arrays := make([][]int64, count)
	for i := range arrays {
		arrays[i] = make([]int64, n)
		for j := range arrays[i] {
			arrays[i][j] = nextRandom() % 101
		}
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		// each round asks every array for a different target up to 300
		for i := int64(0); i < count; i++ {
			a := threeSumMulti(arrays[i], (r*7+i)%301)
			total += a
			check = (check*1000003 + a) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d arrays of %d: answers summing to %d, checksum %d\n", rounds, count, n, total, check)
}
