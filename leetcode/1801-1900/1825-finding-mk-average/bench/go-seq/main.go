// LeetCode #1825: Finding MK Average -- the bench in Go: the fenwick arm over
// 20 calls on windows of 1000 to 49999 numbers, each call adding the same 10^5
// numbers of 1 to 10^5, built once, and asking for the average after every
// hundredth; each window and its cut are drawn from the checksum so far. The
// Fenwick trees are the arm every mirror language writes the same way; the ★
// arm's ordered bags have no counterpart in C, Go or Python's standard
// library.
package main

import "fmt"

const top = 100000

type mkAverage struct {
	m, k   int64
	window []int64
	count  []int64
	total  []int64
}

func newMkAverage(m, k int64) *mkAverage {
	return &mkAverage{m: m, k: k, count: make([]int64, top+1), total: make([]int64, top+1)}
}

func (a *mkAverage) change(x, by int64) {
	for i := x; i <= top; i += i & -i {
		a.count[i] += by
		a.total[i] += by * x
	}
}

// the sum of the t smallest numbers of the window
func (a *mkAverage) smallest(t int64) int64 {
	var at, sum int64
	left := t
	for step := int64(1 << 16); step > 0; step /= 2 {
		if at+step <= top && a.count[at+step] <= left {
			at += step
			left -= a.count[at]
			sum += a.total[at]
		}
	}
	return sum + left*(at+1)
}

func (a *mkAverage) addElement(num int64) {
	a.window = append(a.window, num)
	a.change(num, 1)
	if int64(len(a.window)) > a.m {
		old := a.window[0]
		a.window = a.window[1:]
		a.change(old, -1)
	}
}

func (a *mkAverage) calculateMkAverage() int64 {
	if int64(len(a.window)) < a.m {
		return -1
	}
	return (a.smallest(a.m-a.k) - a.smallest(a.k)) / (a.m - 2*a.k)
}

var seed int64 = 1825

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	nums := make([]int64, 0, 100000)
	for i := 0; i < 100000; i++ {
		hi := nextRandom()
		nums = append(nums, 1+(hi*32768+nextRandom())%100000)
	}
	var check int64
	for call := int64(0); call < 20; call++ {
		m := 1000 + (check+call)%49000
		k := 1 + (check*7+call)%((m-1)/2)
		avg := newMkAverage(m, k)
		for i, x := range nums {
			avg.addElement(x)
			if i%100 == 99 {
				check = (check*31 + avg.calculateMkAverage() + 2) % 1000000007
			}
		}
	}
	fmt.Printf("20 calls: checksum %d\n", check)
}
