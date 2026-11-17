// LeetCode #2241: Design an ATM Machine -- the benchmark's Go mirror of
// atm.kara: the counts of the five banknotes, smallest first; a
// withdrawal plans as many of each as fit, largest first, and takes the
// plan only when it pays the whole amount.
package main

import "fmt"

type Atm struct {
	counts []int64
}

func newAtm() *Atm {
	return &Atm{counts: make([]int64, 5)}
}

func (a *Atm) deposit(banknotesCount []int64) {
	for i := 0; i < 5; i++ {
		a.counts[i] += banknotesCount[i]
	}
}

var values = []int64{20, 50, 100, 200, 500}

func (a *Atm) withdraw(amount int64) []int64 {
	plan := make([]int64, 5)
	left := amount
	for i := 4; i >= 0; i-- {
		plan[i] = min(left/values[i], a.counts[i])
		left -= plan[i] * values[i]
	}
	if left != 0 {
		return []int64{-1}
	}
	for i := 0; i < 5; i++ {
		a.counts[i] -= plan[i]
	}
	return plan
}

var seed int64 = 2241

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	paid := int64(0)
	check := int64(0)
	counts := make([]int64, 5)
	for m := 0; m < 200; m++ {
		atm := newAtm()
		for c := 0; c < 5000; c++ {
			if nextRandom()%2 == 0 {
				for i := 0; i < 5; i++ {
					counts[i] = wideRandom() % 1000000001
				}
				atm.deposit(counts)
			} else {
				amount := (wideRandom()%100000000 + 1) * 10
				answer := atm.withdraw(amount)
				if answer[0] >= 0 {
					paid++
				}
				for _, n := range answer {
					check = (check*31 + n%1000000007 + 1) % 1000000007
				}
			}
		}
	}
	fmt.Printf("200 machines of 5000 calls: %d withdrawals paid, checksum %d\n", paid, check)
}
