// Benchmark for #582: Go mirror of the ★ arm (children lists, walked
// breadth first); see ../kill_process.kara. A map from parent to a slice
// of children with no size hint, and a slice used as the queue.
package main

import "fmt"

func killProcess(pid, ppid []int64, kill int64) []int64 {
	children := map[int64][]int64{}
	for i := range pid {
		children[ppid[i]] = append(children[ppid[i]], pid[i])
	}
	killed := []int64{}
	queue := []int64{kill}
	for head := 0; head < len(queue); head++ {
		p := queue[head]
		killed = append(killed, p)
		queue = append(queue, children[p]...)
	}
	return killed
}

// ---- benchmark --------------------------------------------------------------

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	high := nextRandom(seed) * 32768
	return high + nextRandom(seed)
}

func main() {
	var count int64 = 20
	var rounds int64 = 30
	var n int64 = 50000
	var seed int64 = 582
	pids := make([][]int64, 0, count)
	ppids := make([][]int64, 0, count)
	for g := int64(0); g < count; g++ {
		names := make([]int64, n)
		for i := int64(0); i < n; i++ {
			names[i] = i + 1
		}
		for i := n - 1; i >= 1; i-- {
			j := wide(&seed) % (i + 1)
			names[i], names[j] = names[j], names[i]
		}
		pid := make([]int64, 0, n)
		ppid := make([]int64, 0, n)
		for i := int64(0); i < n; i++ {
			pid = append(pid, names[i])
			if i == 0 {
				ppid = append(ppid, 0)
			} else {
				ppid = append(ppid, names[wide(&seed)%i])
			}
		}
		pids = append(pids, pid)
		ppids = append(ppids, ppid)
	}
	var total int64 = 0
	var checksum int64 = 0
	for round := int64(0); round < rounds; round++ {
		for g := int64(0); g < count; g++ {
			p := (round*7 + g) % count
			var kill int64
			if (round+g)%4 == 0 {
				kill = pids[p][0]
			} else {
				kill = pids[p][wide(&seed)%n]
			}
			got := killProcess(pids[p], ppids[p], kill)
			var sum int64 = 0
			for _, k := range got {
				sum += k
			}
			total += int64(len(got))
			checksum = (checksum*31 + sum) % 1000000007
		}
	}
	fmt.Printf("%d trees of 50000 processes, %d rounds: %d killed, checksum %d\n", count, rounds, total, checksum)
}
