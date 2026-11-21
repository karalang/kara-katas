// LeetCode #2469: Convert the Temperature -- the bench, the ★ arm in Go:
// the two formulas as given, returned in a slice.
package main

import (
	"fmt"
	"math"
)

func convertTemperature(celsius float64) []float64 {
	return []float64{celsius + 273.15, celsius*1.80 + 32.00}
}

func main() {
	// 230 passes over every temperature from 0 to 1000 in hundredths,
	// each pass starting at a hundredth chosen from the checksum so far;
	// every answer's kelvin in hundredths and Fahrenheit in thousandths,
	// rounded, folded into the checksum
	var check int64
	for p := int64(0); p < 230; p++ {
		start := check % 100001
		for i := int64(0); i < 100001; i++ {
			h := (start + i) % 100001
			got := convertTemperature(float64(h) / 100.0)
			kelvin := int64(math.Round(got[0] * 100.0))
			fahrenheit := int64(math.Round(got[1] * 1000.0))
			check = (check*31 + kelvin + fahrenheit + p) % 1000000007
		}
	}
	fmt.Printf("230 passes over every hundredth from 0 to 1000: checksum %d\n", check)
}
