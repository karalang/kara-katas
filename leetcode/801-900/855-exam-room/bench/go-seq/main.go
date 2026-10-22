// Benchmark for #855: Exam Room -- the sorted-vector arm, mirroring
// exam_room.kara.
package main

import (
	"fmt"
	"sort"
)

type ExamRoom struct {
	n     int64
	taken []int64
}

func (r *ExamRoom) seat() int64 {
	if len(r.taken) == 0 {
		r.taken = append(r.taken, 0)
		return 0
	}
	best := r.taken[0]
	bestSeat := int64(0)
	for i := 0; i+1 < len(r.taken); i++ {
		half := (r.taken[i+1] - r.taken[i]) / 2
		if half > best {
			best = half
			bestSeat = r.taken[i] + half
		}
	}
	last := r.taken[len(r.taken)-1]
	if r.n-1-last > best {
		bestSeat = r.n - 1
	}
	lo, hi := 0, len(r.taken)
	for lo < hi {
		mid := (lo + hi) / 2
		if r.taken[mid] < bestSeat {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	r.taken = append(r.taken, 0)
	copy(r.taken[lo+1:], r.taken[lo:])
	r.taken[lo] = bestSeat
	return bestSeat
}

func (r *ExamRoom) leave(p int64) {
	at := sort.Search(len(r.taken), func(i int) bool { return r.taken[i] >= p })
	r.taken = append(r.taken[:at], r.taken[at+1:]...)
}

var seed int64 = 855

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds, calls := 300, 4000
	var n int64 = 1000000000
	var total, checksum int64
	for r := 0; r < rounds; r++ {
		room := &ExamRoom{n: n}
		seated := []int64{}
		for c := 0; c < calls; c++ {
			if len(seated) == 0 || nextRandom()%3 != 0 {
				p := room.seat()
				seated = append(seated, p)
				total += p
				checksum = (checksum*31 + p%1000003) % 1000000007
			} else {
				i := nextRandom() % int64(len(seated))
				p := seated[i]
				seated[i] = seated[len(seated)-1]
				seated = seated[:len(seated)-1]
				room.leave(p)
			}
		}
	}
	fmt.Printf("%d rooms of 4000 calls: seats sum to %d, checksum %d\n", rounds, total, checksum)
}
