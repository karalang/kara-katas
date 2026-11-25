// LeetCode #1390 bench, Go mirror of the ★ arm.
package main

import "fmt"

func sumFourDivisors(nums []int32) int32 {
	var total int32
	for _, v := range nums {
		count := 0
		var sum int32
		var d int32 = 1
		for d*d <= v && count <= 4 {
			if v%d == 0 {
				count++
				sum += d
				if d*d != v {
					count++
					sum += v / d
				}
			}
			d++
		}
		if count == 4 {
			total += sum
		}
	}
	return total
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const n = 10000
	var seed int64 = 1390
	nums := make([]int32, n)
	for k := range nums {
		a := nextRandom(&seed)
		b := nextRandom(&seed)
		nums[k] = int32(1 + (a*32768+b)%100000)
	}
	var check int64
	for r := 0; r < 300; r++ {
		seed = (seed + check) % 2147483648
		i := nextRandom(&seed) % n
		a := nextRandom(&seed)
		b := nextRandom(&seed)
		nums[i] = int32(1 + (a*32768+b)%100000)
		check = (check*131 + int64(sumFourDivisors(nums))) % 1000000007
	}
	fmt.Printf("300 rounds over 10^4 values up to 10^5: checksum %d\n", check)
}
