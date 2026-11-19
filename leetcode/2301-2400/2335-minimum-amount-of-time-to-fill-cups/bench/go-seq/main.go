// LeetCode #2335: Minimum Amount of Time to Fill Cups -- the bench, the ★
// arm in Go: the larger of the most cups of one kind and half of all the
// cups, rounded up.
package main

import "fmt"

func fillCups(amount []int64) int64 {
	most := max(amount[0], amount[1], amount[2])
	return max(most, (amount[0]+amount[1]+amount[2]+1)/2)
}

func main() {
	amount := []int64{0, 0, 0}
	var check int64
	for p := int64(0); p < 3; p++ {
		for a := int64(0); a <= 100; a++ {
			for b := int64(0); b <= 100; b++ {
				for c := int64(0); c <= 100; c++ {
					amount[0] = a
					amount[1] = b
					amount[2] = c
					check = (check*31 + fillCups(amount) + p) % 1000000007
				}
			}
		}
	}
	fmt.Printf("3 passes over 101^3 amounts: checksum %d\n", check)
}
