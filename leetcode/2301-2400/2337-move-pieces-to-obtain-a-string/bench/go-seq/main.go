// LeetCode #2337: Move Pieces to Obtain a String -- the bench, the ★ arm
// in Go: two indices walking the start and the target together, each
// skipping blanks, the pieces matched in order and each `L` no later in
// the target, each `R` no earlier.
package main

import "fmt"

func canChange(a, b string) bool {
	n := len(a)
	i, j := 0, 0
	for {
		for i < n && a[i] == '_' {
			i++
		}
		for j < n && b[j] == '_' {
			j++
		}
		if i == n || j == n {
			return i == n && j == n
		}
		if a[i] != b[j] {
			return false
		}
		if a[i] == 'L' && i < j {
			return false
		}
		if a[i] == 'R' && i > j {
			return false
		}
		i++
		j++
	}
}

func scrambled(index int64) int64 {
	return index * 2654435761 % 2147483647
}

func main() {
	const n = 100000
	starts := make([]string, 10)
	targets := make([]string, 10)
	for q := int64(0); q < 10; q++ {
		cells := make([]byte, n)
		for i := int64(0); i < n; i++ {
			switch scrambled(q*100000+i) % 4 {
			case 0:
				cells[i] = 'L'
			case 1:
				cells[i] = 'R'
			default:
				cells[i] = '_'
			}
		}
		starts[q] = string(cells)
		for round := 0; round < 3; round++ {
			for i := 1; i < n; i++ {
				if cells[i] == 'L' && cells[i-1] == '_' {
					cells[i-1] = 'L'
					cells[i] = '_'
				}
			}
			for i := n - 2; i >= 0; i-- {
				if cells[i] == 'R' && cells[i+1] == '_' {
					cells[i+1] = 'R'
					cells[i] = '_'
				}
			}
		}
		if q%2 == 1 {
			first := 0
			for cells[first] == '_' {
				first++
			}
			if cells[first] == 'L' {
				cells[first] = 'R'
			} else {
				cells[first] = 'L'
			}
		}
		targets[q] = string(cells)
	}
	var check int64
	for p := int64(0); p < 10; p++ {
		for q := 0; q < 10; q++ {
			var can int64 = 1
			if canChange(starts[q], targets[q]) {
				can = 2
			}
			check = (check*31 + can + p) % 1000000007
		}
	}
	fmt.Printf("10 passes over 10 pairs of 10^5 places: checksum %d\n", check)
}
