// LeetCode #1117: Building H2O -- the bench in Go: a goroutine per atom;
// a hydrogen hands a one-shot channel to the oxygens and waits on it, and
// an oxygen takes the bonding lock, receives two hydrogens, releases
// itself, sends each a channel to say it is out on, and waits for both.
package main

import (
	"fmt"
	"strings"
	"sync"
)

type H2O struct {
	bonding   sync.Mutex
	hydrogens chan chan chan struct{}
}

func NewH2O() *H2O {
	return &H2O{hydrogens: make(chan chan chan struct{}, 2)}
}

func (h *H2O) Hydrogen(releaseHydrogen func()) {
	go_ := make(chan chan struct{}, 1)
	h.hydrogens <- go_
	out := <-go_
	releaseHydrogen()
	out <- struct{}{}
}

func (h *H2O) Oxygen(releaseOxygen func()) {
	h.bonding.Lock()
	defer h.bonding.Unlock()
	gos := []chan chan struct{}{<-h.hydrogens, <-h.hydrogens}
	releaseOxygen()
	out := make(chan struct{}, 2)
	for _, g := range gos {
		g <- out
	}
	<-out
	<-out
}

func run(water []byte) string {
	var mu sync.Mutex
	var log strings.Builder
	say := func(s string) func() {
		return func() {
			mu.Lock()
			log.WriteString(s)
			mu.Unlock()
		}
	}
	h := NewH2O()
	var wg sync.WaitGroup
	for _, c := range water {
		wg.Add(1)
		if c == 'H' {
			go func() { defer wg.Done(); h.Hydrogen(say("H")) }()
		} else {
			go func() { defer wg.Done(); h.Oxygen(say("O")) }()
		}
	}
	wg.Wait()
	return log.String()
}

func main() {
	seed := int64(1117)
	whole := 0
	var check int64
	for r := 0; r < 500; r++ {
		water := []byte(strings.Repeat("OHH", 20))
		for j := 0; j < 60; j++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			k := j + int(seed/65536)%(60-j)
			water[j], water[k] = water[k], water[j]
		}
		out := run(water)
		molecules := 0
		for i := 0; i < len(out)/3; i++ {
			if strings.Count(out[3*i:3*i+3], "H") == 2 {
				molecules++
			}
		}
		if molecules == 20 {
			whole++
		}
		check = (check*31 + int64(len(out)) + int64(r)) % 1000000007
	}
	fmt.Printf("500 runs of 20 molecules: %d with every molecule whole, checksum %d\n", whole, check)
}
