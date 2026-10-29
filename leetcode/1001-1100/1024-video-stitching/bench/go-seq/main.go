// LeetCode #1024: Video Stitching -- bench
// Mirrors ../video_stitching.kara; see ../../README.md § Benchmarks.

package main

import "fmt"

func videoStitching(clips [][]int64, time int64) int64 {
	furthest := make([]int64, time+1)
	for _, clip := range clips {
		if clip[0] <= time && clip[1] > furthest[clip[0]] {
			furthest[clip[0]] = clip[1]
		}
	}
	var taken, covered, reach int64
	for t := int64(0); t < time; t++ {
		if furthest[t] > reach {
			reach = furthest[t]
		}
		if reach <= t {
			return -1
		}
		if t == covered {
			taken++
			covered = reach
		}
	}
	return taken
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

type kase struct {
	clips [][]int64
	time  int64
}

func main() {
	count := 2000
	rounds := 500
	seed := int64(1024)
	cases := make([]kase, 0, count)
	totalClips := 0
	for c := 0; c < count; c++ {
		time := 50 + nextRandom(&seed)%51
		clips := [][]int64{}
		at := int64(0)
		for at < time {
			length := 1 + nextRandom(&seed)%10
			back := nextRandom(&seed) % 3
			clips = append(clips, []int64{max(at-back, 0), min(at+length, 100)})
			at += length
		}
		extra := nextRandom(&seed) % (101 - int64(len(clips)))
		for k := int64(0); k < extra; k++ {
			start := nextRandom(&seed) % (time + 1)
			end := min(start+nextRandom(&seed)%21, 100)
			place := nextRandom(&seed) % (int64(len(clips)) + 1)
			clips = append(clips, nil)
			copy(clips[place+1:], clips[place:])
			clips[place] = []int64{start, end}
		}
		totalClips += len(clips)
		cases = append(cases, kase{clips, time})
	}
	var sum, check int64
	for r := 0; r < rounds; r++ {
		for _, cs := range cases {
			answer := videoStitching(cs.clips, cs.time)
			sum += answer
			check = (check*131 + answer + 1) % 1000000007
		}
	}
	fmt.Printf("%d cases, %d clips, %d rounds: sum %d, checksum %d\n", count, totalClips, rounds, sum, check)
}
