// LeetCode #1116: Print Zero Even Odd -- the bench in Go: a goroutine
// per method, three channels of capacity one as the ★ arm's three turn
// channels, zero's filled when the printer is made, and a WaitGroup
// joining the three as Kāra's TaskGroup does.
package main

import (
	"fmt"
	"strconv"
	"strings"
	"sync"
)

type ZeroEvenOdd struct {
	n                           int
	zeroTurn, evenTurn, oddTurn chan struct{}
}

func NewZeroEvenOdd(n int) *ZeroEvenOdd {
	z := &ZeroEvenOdd{n, make(chan struct{}, 1), make(chan struct{}, 1), make(chan struct{}, 1)}
	z.zeroTurn <- struct{}{}
	return z
}

func (z *ZeroEvenOdd) Zero(printNumber func(int)) {
	for i := 1; i <= z.n; i++ {
		<-z.zeroTurn
		printNumber(0)
		if i%2 == 1 {
			z.oddTurn <- struct{}{}
		} else {
			z.evenTurn <- struct{}{}
		}
	}
}

func (z *ZeroEvenOdd) Even(printNumber func(int)) {
	for i := 2; i <= z.n; i += 2 {
		<-z.evenTurn
		printNumber(i)
		z.zeroTurn <- struct{}{}
	}
}

func (z *ZeroEvenOdd) Odd(printNumber func(int)) {
	for i := 1; i <= z.n; i += 2 {
		<-z.oddTurn
		printNumber(i)
		z.zeroTurn <- struct{}{}
	}
}

func run(n int, order []int) string {
	var mu sync.Mutex
	var log strings.Builder
	say := func(x int) {
		mu.Lock()
		log.WriteString(strconv.Itoa(x))
		mu.Unlock()
	}
	z := NewZeroEvenOdd(n)
	var wg sync.WaitGroup
	for _, k := range order {
		wg.Add(1)
		switch k {
		case 0:
			go func() { defer wg.Done(); z.Zero(say) }()
		case 1:
			go func() { defer wg.Done(); z.Even(say) }()
		default:
			go func() { defer wg.Done(); z.Odd(say) }()
		}
	}
	wg.Wait()
	return log.String()
}

func main() {
	orders := [][]int{{0, 1, 2}, {0, 2, 1}, {1, 0, 2}, {1, 2, 0}, {2, 0, 1}, {2, 1, 0}}
	var want strings.Builder
	for i := 1; i <= 200; i++ {
		want.WriteString("0" + strconv.Itoa(i))
	}
	right := 0
	var check int64
	for r := 0; r < 1000; r++ {
		out := run(200, orders[r%6])
		if out == want.String() {
			right++
		}
		check = (check*31 + int64(len(out)) + int64(r)) % 1000000007
	}
	fmt.Printf("1000 runs over 1 to 200: %d in order, checksum %d\n", right, check)
}
