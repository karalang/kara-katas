// LeetCode #1622: Fancy Sequence -- the bench in Go, mirroring fancy.kara:
// every value stored under the inverse of one map x -> mul x + add, the
// inverse a Fermat power per append.
package main

import "fmt"

const MOD int64 = 1000000007

func power(base, exp int64) int64 {
	result, b, e := int64(1), base%MOD, exp
	for e > 0 {
		if e&1 == 1 {
			result = result * b % MOD
		}
		b = b * b % MOD
		e >>= 1
	}
	return result
}

type Fancy struct {
	stored   []int64
	mul, add int64
}

func NewFancy() *Fancy { return &Fancy{mul: 1} }

func (f *Fancy) Append(val int32) {
	shifted := (int64(val) - f.add + MOD) % MOD
	f.stored = append(f.stored, shifted*power(f.mul, MOD-2)%MOD)
}

func (f *Fancy) AddAll(inc int32) { f.add = (f.add + int64(inc)) % MOD }

func (f *Fancy) MultAll(m int32) {
	f.mul = f.mul * int64(m) % MOD
	f.add = f.add * int64(m) % MOD
}

func (f *Fancy) GetIndex(idx int32) int32 {
	if int(idx) >= len(f.stored) {
		return -1
	}
	return int32((f.stored[idx]*f.mul + f.add) % MOD)
}

var seed int64 = 1622

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type call struct {
	kind int64
	arg  int32
}

func main() {
	sequences := make([][]call, 0, 50)
	for s := 0; s < 50; s++ {
		calls := make([]call, 0, 100000)
		var length int64
		for c := 0; c < 100000; c++ {
			arg := nextRandom()%100 + 1
			r := nextRandom() % 10
			switch {
			case r <= 3:
				calls = append(calls, call{0, int32(arg)})
				length++
			case r <= 5:
				calls = append(calls, call{1, int32(arg)})
			case r <= 7:
				calls = append(calls, call{2, int32(arg)})
			default:
				high := nextRandom()
				idx := (high*32768 + nextRandom()) % (length + length/4 + 1)
				calls = append(calls, call{3, int32(idx)})
			}
		}
		sequences = append(sequences, calls)
	}
	var check, misses int64
	for _, calls := range sequences {
		fancy := NewFancy()
		for _, c := range calls {
			switch c.kind {
			case 0:
				fancy.Append(c.arg)
			case 1:
				fancy.AddAll(c.arg)
			case 2:
				fancy.MultAll(c.arg)
			default:
				got := int64(fancy.GetIndex(c.arg))
				if got == -1 {
					misses++
				}
				check = (check*31 + got + 1) % 1000000007
			}
		}
	}
	fmt.Printf("50 sequences of 100000 calls: %d reads past the end, checksum %d\n", misses, check)
}
