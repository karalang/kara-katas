// Benchmark for #380: mirror of randomized_set.kara (the open-addressing
// arm).
package main

import "fmt"

type slot struct {
	val, pos int64
	used     bool
}

type RandomizedSet struct {
	vals  []int64
	slots []slot
	seed  int64
}

func (s *RandomizedSet) home(val int64) int64 {
	h := uint64(val) * 0x9E3779B97F4A7C15
	return int64((h >> 32) & uint64(len(s.slots)-1))
}

func (s *RandomizedSet) find(val int64) int64 {
	mask := int64(len(s.slots) - 1)
	i := s.home(val)
	for {
		if !s.slots[i].used || s.slots[i].val == val {
			return i
		}
		i = (i + 1) & mask
	}
}

func (s *RandomizedSet) setPosition(val, pos int64) {
	s.slots[s.find(val)] = slot{val, pos, true}
}

func (s *RandomizedSet) grow() {
	old := s.slots
	s.slots = make([]slot, 2*len(old))
	for _, sl := range old {
		if sl.used {
			s.setPosition(sl.val, sl.pos)
		}
	}
}

func (s *RandomizedSet) insert(val int64) bool {
	if s.slots[s.find(val)].used {
		return false
	}
	if 2*(len(s.vals)+1) > len(s.slots) {
		s.grow()
	}
	s.setPosition(val, int64(len(s.vals)))
	s.vals = append(s.vals, val)
	return true
}

func (s *RandomizedSet) deleteSlot(i int64) {
	mask := int64(len(s.slots) - 1)
	gap := i
	j := (i + 1) & mask
	s.slots[gap].used = false
	for {
		if !s.slots[j].used {
			return
		}
		h := s.home(s.slots[j].val)
		var stays bool
		if gap <= j {
			stays = gap < h && h <= j
		} else {
			stays = gap < h || h <= j
		}
		if !stays {
			s.slots[gap] = s.slots[j]
			s.slots[j].used = false
			gap = j
		}
		j = (j + 1) & mask
	}
}

func (s *RandomizedSet) remove(val int64) bool {
	i := s.find(val)
	if !s.slots[i].used {
		return false
	}
	pos := s.slots[i].pos
	s.deleteSlot(i)
	last := s.vals[len(s.vals)-1]
	s.vals = s.vals[:len(s.vals)-1]
	if pos < int64(len(s.vals)) {
		s.vals[pos] = last
		s.setPosition(last, pos)
	}
	return true
}

func (s *RandomizedSet) getRandom() int64 {
	s.seed = (s.seed*1103515245 + 12345) % 2147483648
	return s.vals[(s.seed/65536)%int64(len(s.vals))]
}

func main() {
	s := &RandomizedSet{slots: make([]slot, 8), seed: 380}
	seed := int64(380)
	checksum := int64(0)
	for q := 0; q < 20000000; q++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		op := (seed / 65536) % 3
		seed = (seed*1103515245 + 12345) % 2147483648
		x := (seed / 64) % 200000
		var v int64
		switch {
		case op == 0:
			if s.insert(x) {
				v = 1
			}
		case op == 1:
			if s.remove(x) {
				v = 1
			}
		case len(s.vals) > 0:
			v = s.getRandom()
		default:
			v = 7
		}
		checksum = (checksum*31 + v) % 1000000007
	}
	fmt.Printf("checksum %d size %d\n", checksum, len(s.vals))
}
