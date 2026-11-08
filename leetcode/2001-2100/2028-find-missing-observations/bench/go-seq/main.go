// LeetCode #2028: Find Missing Observations -- the ★ arm in Go, the same
// algorithm and workload as observe.kara.
package main

import "fmt"

func missingRolls(rolls []int64, mean, n int64) []int64 {
	var sum int64
	for _, r := range rolls {
		sum += r
	}
	need := mean*(int64(len(rolls))+n) - sum
	if need < n || need > 6*n {
		return []int64{}
	}
	q, r := need/n, need%n
	out := make([]int64, n)
	for i := int64(0); i < n; i++ {
		if i < r {
			out[i] = q + 1
		} else {
			out[i] = q
		}
	}
	return out
}

var seed int64 = 2028

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][]int64, 0, 20)
	means := make([]int64, 0, 20)
	ns := make([]int64, 0, 20)
	for a := 0; a < 20; a++ {
		l := make([]int64, 100000)
		for i := range l {
			l[i] = nextRandom()%6 + 1
		}
		lists = append(lists, l)
		means = append(means, nextRandom()%4+2)
		ns = append(ns, nextRandom()%100000+1)
	}
	var calls, rolls, check int64
	for round := 0; round < 50; round++ {
		for a := 0; a < 20; a++ {
			got := missingRolls(lists[a], means[a], ns[a])
			calls++
			rolls += int64(len(got))
			if len(got) > 0 {
				check = (check*31 + got[0]*7 + got[len(got)-1]) % 1000000007
			} else {
				check = (check*31 + 1) % 1000000007
			}
		}
	}
	fmt.Printf("%d calls: %d rolls, checksum %d\n", calls, rolls, check)
}
