// LeetCode #1195 bench: the ★ arm in Go, over the same 3 runs of
// n = 200000 as the Kāra bench. Go's standard library has no counting
// semaphore, so each is a count under a `sync.Mutex` with a `sync.Cond`.
package main

import (
	"fmt"
	"strconv"
	"sync"
)

type Semaphore struct {
	mu      sync.Mutex
	freed   *sync.Cond
	permits int64
}

func NewSemaphore(permits int64) *Semaphore {
	s := &Semaphore{permits: permits}
	s.freed = sync.NewCond(&s.mu)
	return s
}

func (s *Semaphore) Acquire() {
	s.mu.Lock()
	for s.permits == 0 {
		s.freed.Wait()
	}
	s.permits--
	s.mu.Unlock()
}

func (s *Semaphore) Release() {
	s.mu.Lock()
	s.permits++
	s.mu.Unlock()
	s.freed.Signal()
}

type FizzBuzz struct {
	n                                              int64
	fizzTurn, buzzTurn, fizzbuzzTurn, numberTurn *Semaphore
}

func NewFizzBuzz(n int64) *FizzBuzz {
	return &FizzBuzz{n, NewSemaphore(0), NewSemaphore(0), NewSemaphore(0), NewSemaphore(1)}
}

func (fb *FizzBuzz) pass(i int64) {
	if i > fb.n {
		return
	}
	switch {
	case i%15 == 0:
		fb.fizzbuzzTurn.Release()
	case i%3 == 0:
		fb.fizzTurn.Release()
	case i%5 == 0:
		fb.buzzTurn.Release()
	default:
		fb.numberTurn.Release()
	}
}

func (fb *FizzBuzz) Fizz(printFizz func()) {
	for i := int64(1); i <= fb.n; i++ {
		if i%3 == 0 && i%5 != 0 {
			fb.fizzTurn.Acquire()
			printFizz()
			fb.pass(i + 1)
		}
	}
}

func (fb *FizzBuzz) Buzz(printBuzz func()) {
	for i := int64(1); i <= fb.n; i++ {
		if i%5 == 0 && i%3 != 0 {
			fb.buzzTurn.Acquire()
			printBuzz()
			fb.pass(i + 1)
		}
	}
}

func (fb *FizzBuzz) Fizzbuzz(printFizzbuzz func()) {
	for i := int64(1); i <= fb.n; i++ {
		if i%15 == 0 {
			fb.fizzbuzzTurn.Acquire()
			printFizzbuzz()
			fb.pass(i + 1)
		}
	}
}

func (fb *FizzBuzz) Number(printNumber func(int64)) {
	for i := int64(1); i <= fb.n; i++ {
		if i%3 != 0 && i%5 != 0 {
			fb.numberTurn.Acquire()
			printNumber(i)
			fb.pass(i + 1)
		}
	}
}

func run(n int64, order []int) []string {
	fb := NewFizzBuzz(n)
	var mu sync.Mutex
	var out []string
	put := func(s string) {
		mu.Lock()
		out = append(out, s)
		mu.Unlock()
	}
	var wg sync.WaitGroup
	for _, role := range order {
		wg.Add(1)
		go func(role int) {
			defer wg.Done()
			switch role {
			case 0:
				fb.Fizz(func() { put("fizz") })
			case 1:
				fb.Buzz(func() { put("buzz") })
			case 2:
				fb.Fizzbuzz(func() { put("fizzbuzz") })
			default:
				fb.Number(func(i int64) { put(strconv.FormatInt(i, 10)) })
			}
		}(role)
	}
	wg.Wait()
	return out
}

func main() {
	var check int64
	for _, order := range [][]int{{0, 1, 2, 3}, {3, 2, 1, 0}, {1, 3, 0, 2}} {
		for _, line := range run(200000, order) {
			for i := 0; i < len(line); i++ {
				check = (check*131 + int64(line[i])) % 1000000007
			}
			check = (check*131 + 10) % 1000000007
		}
	}
	fmt.Printf("3 runs of n = 200000: checksum %d\n", check)
}
