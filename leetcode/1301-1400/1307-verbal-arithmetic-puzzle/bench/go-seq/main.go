// LeetCode #1307 bench in Go: the ★ arm (the sum done a column at a time
// from the right with its carry, the result's letter fixed by each column's
// sum) on the same 40 passes of 50 puzzles.
package main

import (
	"fmt"
	"strconv"
)

type puzzle struct {
	// each word and the result as letter numbers, rightmost first
	words  [][]int
	result []int
	leads  []bool
	digit  []int64
	taken  [10]bool
}

func solve(p *puzzle, col, row int, sum int64) bool {
	if col == len(p.result) {
		return sum == 0
	}
	if row == len(p.words) {
		letter := p.result[col]
		d := sum % 10
		if p.digit[letter] >= 0 {
			return p.digit[letter] == d && solve(p, col+1, 0, sum/10)
		}
		if p.taken[d] || (d == 0 && p.leads[letter]) {
			return false
		}
		p.digit[letter] = d
		p.taken[d] = true
		ok := solve(p, col+1, 0, sum/10)
		p.digit[letter] = -1
		p.taken[d] = false
		return ok
	}
	if col >= len(p.words[row]) {
		return solve(p, col, row+1, sum)
	}
	letter := p.words[row][col]
	if p.digit[letter] >= 0 {
		return solve(p, col, row+1, sum+p.digit[letter])
	}
	for d := int64(0); d < 10; d++ {
		if p.taken[d] || (d == 0 && p.leads[letter]) {
			continue
		}
		p.digit[letter] = d
		p.taken[d] = true
		ok := solve(p, col, row+1, sum+d)
		p.digit[letter] = -1
		p.taken[d] = false
		if ok {
			return true
		}
	}
	return false
}

func isSolvable(words []string, result string) bool {
	for _, w := range words {
		if len(w) > len(result) {
			return false
		}
	}
	number := [26]int{}
	for k := range number {
		number[k] = -1
	}
	var leads []bool
	var rows [][]int
	texts := append(append([]string{}, words...), result)
	for _, text := range texts {
		row := []int{}
		for k := 0; k < len(text); k++ {
			c := int(text[k] - 'A')
			if number[c] < 0 {
				number[c] = len(leads)
				leads = append(leads, false)
			}
			row = append(row, number[c])
		}
		if len(row) > 1 {
			leads[row[0]] = true
		}
		for a, b := 0, len(row)-1; a < b; a, b = a+1, b-1 {
			row[a], row[b] = row[b], row[a]
		}
		rows = append(rows, row)
	}
	resultRow := rows[len(rows)-1]
	rows = rows[:len(rows)-1]
	digit := make([]int64, len(leads))
	for k := range digit {
		digit[k] = -1
	}
	p := &puzzle{words: rows, result: resultRow, leads: leads, digit: digit}
	return solve(p, 0, 0, 0)
}

var seed int64

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var check int64
	for pass := int64(0); pass < 40; pass++ {
		seed = check
		var solvable int64
		for p := 0; p < 50; p++ {
			letter := []byte("ABCDEFGHIJ")
			for k := 9; k >= 1; k-- {
				j := nextRandom() % int64(k+1)
				letter[k], letter[j] = letter[j], letter[k]
			}
			count := 2 + nextRandom()%4
			var numbers []int64
			var total int64
			for w := int64(0); w < count; w++ {
				digits := 1 + nextRandom()%6
				low := int64(1)
				for k := int64(1); k < digits; k++ {
					low *= 10
				}
				var value int64
				if digits == 1 {
					value = nextRandom() % 10
				} else {
					value = low + nextRandom()%(9*low)
				}
				numbers = append(numbers, value)
				total += value
			}
			numbers = append(numbers, total)
			var texts []string
			for _, v := range numbers {
				s := []byte(strconv.FormatInt(v, 10))
				for k := range s {
					s[k] = letter[s[k]-'0']
				}
				texts = append(texts, string(s))
			}
			result := []byte(texts[len(texts)-1])
			texts = texts[:len(texts)-1]
			if p%2 == 1 {
				at := nextRandom() % int64(len(result))
				result[at] = letter[nextRandom()%10]
			}
			if isSolvable(texts, string(result)) {
				solvable++
			}
		}
		check = (check*31 + solvable + pass) % 1000000007
	}
	fmt.Printf("40 passes of 50 puzzles: checksum %d\n", check)
}
