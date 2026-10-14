// LeetCode 631 -- Design Excel Sum Formula, bench mirror in Go.
//
// The rebuild arm of excel.kara: every formula is the list of cells it
// reads, and after each write a depth-first walk orders the formula
// cells and recomputes them all. Same 2,000 operations, same 60 rounds,
// same output line.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

type Excel struct {
	width    int64
	values   []int64
	formulas [][]int64 // nil means no formula
}

func newExcel(height int64, width byte) *Excel {
	columns := int64(width-'A') + 1
	return &Excel{
		width:    columns,
		values:   make([]int64, height*columns),
		formulas: make([][]int64, height*columns),
	}
}

func (e *Excel) set(row int64, column byte, val int64) {
	at := e.cell(row, column)
	e.values[at] = val
	e.formulas[at] = nil
	e.recompute()
}

func (e *Excel) get(row int64, column byte) int64 {
	return e.values[e.cell(row, column)]
}

func (e *Excel) sum(row int64, column byte, numbers []string) int64 {
	at := e.cell(row, column)
	reads := []int64{}
	for _, rng := range numbers {
		ends := strings.Split(rng, ":")
		top, left := e.position(ends[0])
		bottom, right := e.position(ends[len(ends)-1])
		for r := top; r < bottom+1; r++ {
			for c := left; c < right+1; c++ {
				reads = append(reads, r*e.width+c)
			}
		}
	}
	e.formulas[at] = reads
	e.recompute()
	return e.values[at]
}

func (e *Excel) cell(row int64, column byte) int64 {
	return (row-1)*e.width + int64(column-'A')
}

// The zero-based row and column of a name such as `B12`.
func (e *Excel) position(name string) (int64, int64) {
	column := int64(name[0] - 'A')
	row, _ := strconv.ParseInt(name[1:], 10, 64)
	return row - 1, column
}

func (e *Excel) recompute() {
	seen := make([]bool, len(e.values))
	order := []int64{}
	for at := int64(0); at < int64(len(e.values)); at++ {
		visit(e.formulas, at, seen, &order)
	}
	for _, at := range order {
		if reads := e.formulas[at]; reads != nil {
			var total int64
			for _, source := range reads {
				total += e.values[source]
			}
			e.values[at] = total
		}
	}
}

// Append `at` to `order` after every cell its formula reads.
func visit(formulas [][]int64, at int64, seen []bool, order *[]int64) {
	if seen[at] {
		return
	}
	seen[at] = true
	if reads := formulas[at]; reads != nil {
		for _, source := range reads {
			visit(formulas, source, seen, order)
		}
	}
	*order = append(*order, at)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func letter(index int64) byte { return byte('A' + index) }

type Op struct {
	kind, row, val int64
	column         byte
	ranges         []string
}

func makeOps(count int64, seed *int64) []Op {
	ops := []Op{}
	for i := int64(0); i < count; i++ {
		kind := nextRandom(seed) % 3
		row := 1 + nextRandom(seed)%26
		column := letter(nextRandom(seed) % 26)
		var val int64
		ranges := []string{}
		if kind == 0 {
			val = nextRandom(seed)%2001 - 1000
		} else if kind == 1 && row > 1 {
			n := 1 + nextRandom(seed)%3
			for k := int64(0); k < n; k++ {
				top := 1 + nextRandom(seed)%(row-1)
				left := nextRandom(seed) % 26
				bottom := min(top+nextRandom(seed)%2, row-1)
				right := min(left+nextRandom(seed)%2, 25)
				if top == bottom && left == right {
					ranges = append(ranges, fmt.Sprintf("%c%d", letter(left), top))
				} else {
					ranges = append(ranges, fmt.Sprintf("%c%d:%c%d", letter(left), top, letter(right), bottom))
				}
			}
		} else {
			kind = 2
		}
		ops = append(ops, Op{kind: kind, row: row, column: column, val: val, ranges: ranges})
	}
	return ops
}

func main() {
	seed := int64(631)
	ops := makeOps(2000, &seed)
	rounds := 60
	var sums, checksum, total int64
	for round := 0; round < rounds; round++ {
		sheet := newExcel(26, 'Z')
		for i := range ops {
			op := &ops[i]
			var result int64
			if op.kind == 0 {
				sheet.set(op.row, op.column, op.val)
			} else if op.kind == 1 {
				result = sheet.sum(op.row, op.column, op.ranges)
				sums++
			} else {
				result = sheet.get(op.row, op.column)
			}
			checksum = ((checksum*31+result)%1000000007 + 1000000007) % 1000000007
		}
		for row := int64(1); row < 27; row++ {
			for c := int64(0); c < 26; c++ {
				total += sheet.get(row, letter(c))
			}
		}
	}
	fmt.Printf("%d operations, %d rounds (%d sums): checksum %d, sheet total %d\n", len(ops), rounds, sums, checksum, total)
}
