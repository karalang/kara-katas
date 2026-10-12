// Benchmark for #396: mirror of rotate_function.kara (one rotation from the last).
package main

import "fmt"

func maxRotateFunction(nums []int64) int64 {
	n := int64(len(nums))
	var sum, f int64
	for i := int64(0); i < n; i++ {
		sum += nums[i]
		f += i * nums[i]
	}
	best := f
	for k := int64(1); k < n; k++ {
		f = f + sum - n*nums[n-k]
		if f > best {
			best = f
		}
	}
	return best
}

var seed int64 = 396

func step() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	windows := 2000
	pool := make([]int64, 1000000)
	for i := range pool {
		pool[i] = step()%201 - 100
	}
	const m = 1000000007
	var total, checksum int64
	for w := 0; w < windows; w++ {
		hi := step()
		a := (hi*32768 + step()) % (1000000 - 100000)
		r := maxRotateFunction(pool[a : a+100000])
		total += r
		checksum = (checksum*31 + r%m + m) % m
	}
	fmt.Printf("%d windows: total %d, checksum %d\n", windows, total, checksum)
}
