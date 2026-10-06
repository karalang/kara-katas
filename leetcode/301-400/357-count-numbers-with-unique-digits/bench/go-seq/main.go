// Benchmark for #357 -- same workload and algorithm as unique_digits.kara.
package main

import "fmt"

func extend(length, n, base, used int64) int64 {
	if length == n {
		return 1
	}
	var count int64 = 1
	for d := int64(0); d < base; d++ {
		if length == 0 && d == 0 {
			continue
		}
		if used&(1<<d) == 0 {
			count += extend(length+1, n, base, used|(1<<d))
		}
	}
	return count
}

func main() {
	var checksum int64 = 0
	for base := int64(2); base <= 11; base++ {
		count := extend(0, base, base, 0)
		checksum = (checksum*31 + count) % 1000000007
	}
	fmt.Printf("bases 2 to 11: checksum %d\n", checksum)
}
