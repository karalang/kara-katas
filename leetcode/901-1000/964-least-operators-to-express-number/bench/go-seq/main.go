// Benchmark: LeetCode #964 Least Operators to Express Number -- the ★
// arm, digit DP, on every x from 2 to 100 and 2000 targets spread below
// LeetCode's largest, 2 * 10^8, each round's targets one higher than the
// last's. Mirrors ../least_ops_express_target.kara, .c, .rs and .py.
package main

import "fmt"

func leastOpsExpressTarget(x, target int64) int64 {
	t := target
	var pos, neg, k int64
	for t > 0 {
		cur := t % x
		t /= x
		if k > 0 {
			p := min(cur*k+pos, (cur+1)*k+neg)
			n := min((x-cur)*k+pos, (x-cur-1)*k+neg)
			pos, neg = p, n
		} else {
			pos, neg = cur*2, (x-cur)*2
		}
		k++
	}
	return min(pos, k+neg) - 1
}

func main() {
	rounds := 80
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for x := int64(2); x < 101; x++ {
			for j := int64(0); j < 2000; j++ {
				n := leastOpsExpressTarget(x, 200000000-99991*j-r)
				total += n
				check = (check*31 + n) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds over x from 2 to 100 and 2000 targets: %d operators, checksum %d\n", rounds, total, check)
}
