// LeetCode #2162: Minimum Cost to Set Cooking Time -- the benchmark's Go
// mirror of cooking.kara.
package main

import (
	"fmt"
	"math"
	"strconv"
)

func cost(digits string, startAt, moveCost, pushCost int64) int64 {
	at, total := startAt, int64(0)
	for i := 0; i < len(digits); i++ {
		d := int64(digits[i] - '0')
		if d != at {
			total += moveCost
			at = d
		}
		total += pushCost
	}
	return total
}

func minCostSetTime(startAt, moveCost, pushCost, targetSeconds int64) int64 {
	minutes, seconds := targetSeconds/60, targetSeconds%60
	best := int64(math.MaxInt64)
	for _, w := range [2][2]int64{{minutes, seconds}, {minutes - 1, seconds + 60}} {
		m, s := w[0], w[1]
		if m >= 0 && m <= 99 && s <= 99 {
			if c := cost(strconv.FormatInt(m*100+s, 10), startAt, moveCost, pushCost); c < best {
				best = c
			}
		}
	}
	return best
}

func main() {
	var total, check int64
	for pass := int64(0); pass < 30; pass++ {
		moveCost, pushCost := pass%10+1, pass*3%10+1
		for startAt := int64(0); startAt < 10; startAt++ {
			for target := int64(1); target < 6040; target++ {
				c := minCostSetTime(startAt, moveCost, pushCost, target)
				total += c
				check = (check*31 + c + pass) % 1000000007
			}
		}
	}
	fmt.Printf("1811700 solves: %d in all, checksum %d\n", total, check)
}
