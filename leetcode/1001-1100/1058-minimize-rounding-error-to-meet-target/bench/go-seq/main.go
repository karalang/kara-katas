// LeetCode #1058: Minimize Rounding Error to Meet Target -- the benchmark,
// the same algorithm as rounding.kara.
package main

import (
	"fmt"
	"sort"
)

func thousandths(p string) int64 {
	var value int64
	for _, c := range p {
		if c != '.' {
			value = value*10 + int64(c-'0')
		}
	}
	return value
}

func minimizeError(prices []string, target int64) string {
	var floorSum int64
	fractions := []int64{}
	for _, p := range prices {
		t := thousandths(p)
		floorSum += t / 1000
		if t%1000 != 0 {
			fractions = append(fractions, t%1000)
		}
	}
	up := target - floorSum
	if up < 0 || up > int64(len(fractions)) {
		return "-1"
	}
	sort.Slice(fractions, func(a, b int) bool { return fractions[a] > fractions[b] })
	var errSum int64
	for k, f := range fractions {
		if int64(k) < up {
			errSum += 1000 - f
		} else {
			errSum += f
		}
	}
	return fmt.Sprintf("%d.%03d", errSum/1000, errSum%1000)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomPrice(seed *int64) string {
	whole := nextRandom(seed) % 1000
	var part int64
	if nextRandom(seed)%4 != 0 {
		part = nextRandom(seed)%999 + 1
	}
	return fmt.Sprintf("%d.%03d", whole, part)
}

func main() {
	seed := int64(1058)
	lists := make([][]string, 0, 40)
	for l := 0; l < 40; l++ {
		prices := make([]string, 0, 500)
		for i := 0; i < 500; i++ {
			prices = append(prices, randomPrice(&seed))
		}
		lists = append(lists, prices)
	}
	var calls, check int64
	for round := 0; round < 8; round++ {
		for _, prices := range lists {
			var floorSum, withFraction int64
			for _, p := range prices {
				t := thousandths(p)
				floorSum += t / 1000
				if t%1000 != 0 {
					withFraction++
				}
			}
			for target := floorSum - 1; target < floorSum+withFraction+2; target++ {
				answer := minimizeError(prices, target)
				for _, c := range []byte(answer) {
					check = (check*131 + int64(c)) % 1000000007
				}
				calls++
			}
		}
	}
	fmt.Printf("%d calls: checksum %d\n", calls, check)
}
