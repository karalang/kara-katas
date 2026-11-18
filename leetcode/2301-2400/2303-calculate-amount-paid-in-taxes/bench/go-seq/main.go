// LeetCode #2303: Calculate Amount Paid in Taxes -- the bench, the ★ arm
// in Go. Walk the brackets in order, taxing the part of the income inside
// each at its percent, summed in hundredths and divided once at the end.
package main

import (
	"fmt"
	"math"
)

func calculateTax(brackets [][2]int64, income int64) float64 {
	var hundredths, below int64
	for _, b := range brackets {
		if below >= income {
			break
		}
		upper := b[0]
		if income < upper {
			upper = income
		}
		hundredths += (upper - below) * b[1]
		below = b[0]
	}
	return float64(hundredths) / 100.0
}

var seed int64 = 2303

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][][2]int64, 20)
	for a := range lists {
		brackets := make([][2]int64, 100)
		for i := int64(0); i < 100; i++ {
			var less int64
			if i != 99 {
				less = nextRandom() % 5
			}
			brackets[i] = [2]int64{10*(i+1) - less, nextRandom() % 101}
		}
		lists[a] = brackets
	}
	var check int64
	for p := 0; p < 100; p++ {
		for _, brackets := range lists {
			for income := int64(0); income <= 1000; income++ {
				tax := int64(math.Round(calculateTax(brackets, income) * 100.0))
				check = (check*31 + tax) % 1000000007
			}
		}
	}
	fmt.Printf("100 passes over 20 lists of 100 brackets and 1001 incomes: checksum %d\n", check)
}
