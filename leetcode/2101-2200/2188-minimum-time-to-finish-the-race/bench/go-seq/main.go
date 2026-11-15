// LeetCode #2188: Minimum Time to Finish the Race -- the benchmark's Go
// mirror of race.kara, over a slice of the row: the runs on one tire,
// then the laps bottom up.
package main

import "fmt"

func minimumFinishTime(tires [][2]int64, changeTime, numLaps int64) int64 {
	run := []int64{0}
	for _, t := range tires {
		f, r := t[0], t[1]
		lap, sum, k := f, int64(0), int64(1)
		for k <= numLaps && lap <= changeTime+f {
			sum += lap
			if int(k) == len(run) {
				run = append(run, sum)
			} else if sum < run[k] {
				run[k] = sum
			}
			lap *= r
			k++
		}
	}
	best := make([]int64, numLaps+1)
	for n := int64(1); n <= numLaps; n++ {
		least := run[1]*n + changeTime*(n-1)
		for k := int64(1); int(k) < len(run) && k <= n; k++ {
			pit := changeTime
			if k == n {
				pit = 0
			}
			if t := best[n-k] + pit + run[k]; t < least {
				least = t
			}
		}
		best[n] = least
	}
	return best[numLaps]
}

var seed int64 = 2188

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func bigRandom() int64 {
	a := nextRandom()
	b := nextRandom()
	return a*32768 + b
}

func main() {
	row := make([][2]int64, 100000)
	for i := range row {
		row[i][0] = bigRandom()%100 + 1
		row[i][1] = nextRandom()%4 + 2
	}
	var check int64
	for s := 0; s < 5000; s++ {
		start := bigRandom() % 99901
		changeTime := bigRandom()%100000 + 1
		numLaps := int64(1000)
		t := minimumFinishTime(row[start:start+100], changeTime, numLaps)
		check = (check*31 + t%1000000007) % 1000000007
	}
	fmt.Printf("5000 solves: checksum %d\n", check)
}
