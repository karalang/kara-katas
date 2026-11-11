// LeetCode #1115: Print FooBar Alternately -- the bench in Go: a
// goroutine per method, two channels of capacity one as the ★ arm's two
// turn channels, foo's filled when the pair is made, and a WaitGroup
// joining the two as Kāra's TaskGroup does.
package main

import (
	"fmt"
	"strings"
	"sync"
)

type FooBar struct {
	n                int
	fooTurn, barTurn chan struct{}
}

func NewFooBar(n int) *FooBar {
	fb := &FooBar{n, make(chan struct{}, 1), make(chan struct{}, 1)}
	fb.fooTurn <- struct{}{}
	return fb
}

func (fb *FooBar) Foo(printFoo func()) {
	for i := 0; i < fb.n; i++ {
		<-fb.fooTurn
		printFoo()
		fb.barTurn <- struct{}{}
	}
}

func (fb *FooBar) Bar(printBar func()) {
	for i := 0; i < fb.n; i++ {
		<-fb.barTurn
		printBar()
		fb.fooTurn <- struct{}{}
	}
}

func run(n int, barFirst bool) string {
	var mu sync.Mutex
	var log strings.Builder
	write := func(s string) func() {
		return func() {
			mu.Lock()
			log.WriteString(s)
			mu.Unlock()
		}
	}
	fb := NewFooBar(n)
	var wg sync.WaitGroup
	wg.Add(2)
	foo := func() { defer wg.Done(); fb.Foo(write("foo")) }
	bar := func() { defer wg.Done(); fb.Bar(write("bar")) }
	if barFirst {
		go bar()
		go foo()
	} else {
		go foo()
		go bar()
	}
	wg.Wait()
	return log.String()
}

func main() {
	want := strings.Repeat("foobar", 200)
	alternating := 0
	var check int64
	for r := 0; r < 1000; r++ {
		out := run(200, r%2 == 1)
		if out == want {
			alternating++
		}
		check = (check*31 + int64(len(out)) + int64(r)) % 1000000007
	}
	fmt.Printf("1000 runs of 200 rounds: %d alternating, checksum %d\n", alternating, check)
}
