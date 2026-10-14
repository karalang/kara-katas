// Benchmark for #568: Go mirror of the ★ arm (dynamic programming over
// the weeks); see max_vacation_days.kara.
package main

import "fmt"

func maxVacationDays(flights, days [][]int64) int64 {
	n := len(flights)
	k := len(days[0])
	best := make([]int64, n)
	for c := range best {
		best[c] = -1
	}
	best[0] = 0
	for w := 0; w < k; w++ {
		next := make([]int64, n)
		for c := range next {
			next[c] = -1
		}
		for j := 0; j < n; j++ {
			for i := 0; i < n; i++ {
				if best[i] >= 0 && (i == j || flights[i][j] == 1) {
					next[j] = max(next[j], best[i]+days[j][w])
				}
			}
		}
		best = next
	}
	answer := best[0]
	for _, b := range best {
		answer = max(answer, b)
	}
	return answer
}

// ---- benchmark --------------------------------------------------------------

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	var count int64 = 20
	var rounds int64 = 30
	densities := []int64{1, 2, 5, 10, 25, 50, 100}
	var seed int64 = 568
	flightsOf := make([][][]int64, 0, count)
	daysOf := make([][][]int64, 0, count)
	for g := int64(0); g < count; g++ {
		density := densities[g%7]
		flights := make([][]int64, 0, 100)
		for i := 0; i < 100; i++ {
			row := make([]int64, 100)
			for j := 0; j < 100; j++ {
				if i != j && step(&seed)%100 < density {
					row[j] = 1
				}
			}
			flights = append(flights, row)
		}
		days := make([][]int64, 0, 100)
		for c := 0; c < 100; c++ {
			row := make([]int64, 100)
			for w := 0; w < 100; w++ {
				row[w] = step(&seed) % 8
			}
			days = append(days, row)
		}
		flightsOf = append(flightsOf, flights)
		daysOf = append(daysOf, days)
	}
	var total int64 = 0
	var checksum int64 = 0
	for round := int64(0); round < rounds; round++ {
		for g := int64(0); g < count; g++ {
			p := (round*7 + g) % count
			got := maxVacationDays(flightsOf[p], daysOf[p])
			total += got
			checksum = (checksum*31 + got + 1) % 1000000007
		}
	}
	fmt.Printf("%d cases of 100 cities and 100 weeks, %d rounds: %d days, checksum %d\n", count, rounds, total, checksum)
}
