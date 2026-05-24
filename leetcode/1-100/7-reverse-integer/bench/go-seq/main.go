// LeetCode 7 — pop-and-push Reverse Integer, Go seq mirror.
package main

import "fmt"

func reverse(x int32) int32 {
	var result int32
	const intMax int32 = 2147483647
	const intMin int32 = -2147483648
	const maxDiv int32 = intMax / 10
	const minDiv int32 = intMin / 10

	for x != 0 {
		digit := x % 10
		if result > maxDiv || (result == maxDiv && digit > 7) {
			return 0
		}
		if result < minDiv || (result == minDiv && digit < -8) {
			return 0
		}
		result = result*10 + digit
		x /= 10
	}
	return result
}

func main() {
	const n int64 = 1024
	const kIters int64 = 50_000_000

	inputs := make([]int32, n)
	for i := int64(0); i < n; i++ {
		raw := i*2654435769 + 305419896
		inputs[i] = int32(raw)
	}

	var sum int64
	for k := int64(0); k < kIters; k++ {
		idx := k % n
		sum += int64(reverse(inputs[idx]))
	}
	fmt.Println(sum)
}
