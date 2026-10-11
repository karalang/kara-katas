// Benchmark for #365 -- mirror of water_jug.kara.
package main

import "fmt"

func gcd(a, b int64) int64 {
	if b == 0 {
		return a
	}
	return gcd(b, a%b)
}

func canMeasureWater(x, y, target int64) bool {
	return target <= x+y && target%gcd(x, y) == 0
}

func main() {
	var seed int64 = 365
	var yes, checksum int64
	for i := int64(0); i < 5000000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		x := 1 + (seed/65536)%1000000
		seed = (seed*1103515245 + 12345) % 2147483648
		y := 1 + (seed/65536)%1000000
		seed = (seed*1103515245 + 12345) % 2147483648
		target := ((seed / 65536) % 1000) * (1 + i%6)
		if canMeasureWater(x, y, target) {
			yes++
			checksum = (checksum*31 + i) % 1000000007
		}
	}
	fmt.Printf("%d measurable, checksum %d\n", yes, checksum)
}
