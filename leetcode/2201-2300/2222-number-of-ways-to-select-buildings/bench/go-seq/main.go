// LeetCode #2222: Number of Ways to Select Buildings -- bench mirror of
// buildings.kara: one pass keeping the 0s and 1s behind and the pairs
// "01" and "10", each character closing the pairs it completes.
package main

import "fmt"

func numberOfWays(s string) int64 {
	var zeros, ones, zeroOnes, oneZeros, ways int64
	for _, c := range s {
		if c == '0' {
			ways += zeroOnes
			oneZeros += ones
			zeros++
		} else {
			ways += oneZeros
			zeroOnes += zeros
			ones++
		}
	}
	return ways
}

var seed int64 = 2222

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func building() byte {
	if nextRandom()%2 == 1 {
		return '1'
	}
	return '0'
}

func main() {
	var streets [][]byte
	for a := 0; a < 30; a++ {
		// 10^5 buildings, each a 1 with chance one half
		street := make([]byte, 100000)
		for i := range street {
			street[i] = building()
		}
		streets = append(streets, street)
	}
	var check int64
	for a := 0; a < 30; a++ {
		for r := 0; r < 10; r++ {
			// punch: one building is drawn again before each answer
			streets[a][r*9999] = building()
			s := string(streets[a])
			check = (check*31 + numberOfWays(s)) % 1000000007
		}
	}
	fmt.Printf("30 streets of 10^5, 10 punches: checksum %d\n", check)
}
