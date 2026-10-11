// Benchmark for #367 -- mirror of perfect_square.kara.
package main

import "fmt"

func isPerfectSquare(num int64) bool {
	lo, hi := int64(1), num
	for lo <= hi {
		mid := lo + (hi-lo)/2
		sq := mid * mid
		if sq == num {
			return true
		}
		if sq < num {
			lo = mid + 1
		} else {
			hi = mid - 1
		}
	}
	return false
}

func main() {
	var seed int64 = 367
	var yes, checksum int64
	for i := int64(0); i < 3000000; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		high := seed / 65536
		seed = (seed*1103515245 + 12345) % 2147483648
		wide := high*32768 + seed/65536
		var num int64
		if i%2 == 0 {
			r := 1 + wide%46340
			num = r * r
		} else {
			num = 1 + wide + (i/2%2)*1073741823
		}
		if isPerfectSquare(num) {
			yes++
			checksum = (checksum*31 + i) % 1000000007
		}
	}
	fmt.Printf("%d squares, checksum %d\n", yes, checksum)
}
