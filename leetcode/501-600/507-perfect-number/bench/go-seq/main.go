// Benchmark for #507 in Go: the ★ arm (divisors in pairs up to the
// square root); see ../../check_perfect_number.kara.
package main

import "fmt"

func checkPerfectNumber(num int64) bool {
	if num == 1 {
		return false
	}
	sum := int64(1)
	for i := int64(2); i*i <= num; i++ {
		if num%i == 0 {
			sum += i
			if i*i != num {
				sum += num / i
			}
		}
	}
	return sum == num
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 100,000 numbers from 1 to 10^8 (the problem's most), one in ten of
	// them one of the five perfect numbers in range, built once. Then
	// each is checked once.
	count := 100000
	known := []int64{6, 28, 496, 8128, 33550336}
	seed := int64(507)
	nums := make([]int64, 0, count)
	for c := 0; c < count; c++ {
		if c%10 == 0 {
			nums = append(nums, known[nextRandom(&seed)%5])
		} else {
			hi := nextRandom(&seed)
			lo := nextRandom(&seed)
			nums = append(nums, 1+(hi*32768+lo)%100000000)
		}
	}
	var perfect, checksum int64
	for _, num := range nums {
		answer := checkPerfectNumber(num)
		bit := int64(0)
		if answer {
			perfect++
			bit = 1
		}
		checksum = (checksum*31 + num%1000*2 + bit) % 1000000007
	}
	fmt.Printf("%d numbers: %d perfect, checksum %d\n", count, perfect, checksum)
}
