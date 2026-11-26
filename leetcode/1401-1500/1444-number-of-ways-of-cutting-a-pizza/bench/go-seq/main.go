package main

import "fmt"

// The Go mirror of ways.kara: the same suffix sums and table, a fresh table
// for each count of pieces, as the Kara arm makes a fresh Vec.
func table(rows, cols int) [][]int64 {
	t := make([][]int64, rows+1)
	for i := range t {
		t[i] = make([]int64, cols+1)
	}
	return t
}

func ways(pizza []string, k int) int32 {
	rows, cols := len(pizza), len(pizza[0])
	apples := table(rows, cols)
	for r := rows - 1; r >= 0; r-- {
		for c := cols - 1; c >= 0; c-- {
			here := int64(0)
			if pizza[r][c] == 'A' {
				here = 1
			}
			apples[r][c] = here + apples[r+1][c] + apples[r][c+1] - apples[r+1][c+1]
		}
	}
	w := table(rows, cols)
	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			if apples[r][c] > 0 {
				w[r][c] = 1
			}
		}
	}
	for p := 1; p < k; p++ {
		next := table(rows, cols)
		for r := 0; r < rows; r++ {
			for c := 0; c < cols; c++ {
				total := int64(0)
				for cut := r + 1; cut < rows; cut++ {
					if apples[r][c]-apples[cut][c] > 0 {
						total += w[cut][c]
					}
				}
				for cut := c + 1; cut < cols; cut++ {
					if apples[r][c]-apples[r][cut] > 0 {
						total += w[r][cut]
					}
				}
				next[r][c] = total % 1000000007
			}
		}
		w = next
	}
	return int32(w[0][0])
}

func main() {
	seed, check := int64(1444), int64(0)
	for t := 0; t < 200; t++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		rate := 5 + seed/65536%46
		pizza := []string{}
		for r := 0; r < 50; r++ {
			line := make([]byte, 50)
			for c := 0; c < 50; c++ {
				seed = (seed*1103515245 + 12345) % 2147483648
				if seed/65536%100 < rate {
					line[c] = 'A'
				} else {
					line[c] = '.'
				}
			}
			pizza = append(pizza, string(line))
		}
		check = (check*131 + int64(ways(pizza, 10))) % 1000000007
	}
	fmt.Printf("200 pizzas of 50 by 50: checksum %d\n", check)
}
