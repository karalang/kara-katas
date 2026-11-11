// LeetCode #1114: Print in Order -- the bench in Go: a goroutine per
// method, two channels of capacity one as the ★ arm's, and a WaitGroup
// joining the three as Kāra's TaskGroup does.
package main

import (
	"fmt"
	"strings"
	"sync"
)

type Foo struct {
	firstDone, secondDone chan struct{}
}

func NewFoo() *Foo {
	return &Foo{make(chan struct{}, 1), make(chan struct{}, 1)}
}

func (f *Foo) First(printFirst func()) {
	printFirst()
	f.firstDone <- struct{}{}
}

func (f *Foo) Second(printSecond func()) {
	<-f.firstDone
	printSecond()
	f.secondDone <- struct{}{}
}

func (f *Foo) Third(printThird func()) {
	<-f.secondDone
	printThird()
}

func run(nums []int) string {
	var mu sync.Mutex
	var log strings.Builder
	write := func(s string) func() {
		return func() {
			mu.Lock()
			log.WriteString(s)
			mu.Unlock()
		}
	}
	foo := NewFoo()
	var wg sync.WaitGroup
	for _, k := range nums {
		wg.Add(1)
		switch k {
		case 1:
			go func() { defer wg.Done(); foo.First(write("first")) }()
		case 2:
			go func() { defer wg.Done(); foo.Second(write("second")) }()
		default:
			go func() { defer wg.Done(); foo.Third(write("third")) }()
		}
	}
	wg.Wait()
	return log.String()
}

func main() {
	orders := [][]int{{1, 2, 3}, {1, 3, 2}, {2, 1, 3}, {2, 3, 1}, {3, 1, 2}, {3, 2, 1}}
	inOrder := 0
	var check int64
	for r := 0; r < 10000; r++ {
		out := run(orders[r*7%6])
		if out == "firstsecondthird" {
			inOrder++
		}
		check = (check*31 + int64(len(out))) % 1000000007
	}
	fmt.Printf("10000 runs: %d printed in order, checksum %d\n", inOrder, check)
}
