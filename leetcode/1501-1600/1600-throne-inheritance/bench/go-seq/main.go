// LeetCode #1600: Throne Inheritance
// -- the bench in Go, mirroring throne.kara: each person's children in a
// map[string][]string, the dead in a map[string]bool, the preorder
// walked with a stack, through 10 reigns of 50000 calls, drawn first.
package main

import "fmt"

type ThroneInheritance struct {
	king     string
	children map[string][]string
	dead     map[string]bool
}

func newThrone(king string) *ThroneInheritance {
	return &ThroneInheritance{king, map[string][]string{}, map[string]bool{}}
}

func (t *ThroneInheritance) birth(parent, child string) {
	t.children[parent] = append(t.children[parent], child)
}

func (t *ThroneInheritance) death(name string) {
	t.dead[name] = true
}

func (t *ThroneInheritance) getInheritanceOrder() []string {
	var order []string
	stack := []string{t.king}
	for len(stack) > 0 {
		name := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		if !t.dead[name] {
			order = append(order, name)
		}
		kids := t.children[name]
		for i := len(kids) - 1; i >= 0; i-- {
			stack = append(stack, kids[i])
		}
	}
	return order
}

type op struct {
	kind int
	a, b string
}

var seed int64 = 1600

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	reigns := make([][]op, 10)
	for g := range reigns {
		alive := []string{"king"}
		born := 0
		var ops []op
		for i := 0; i < 50000; i++ {
			r := nextRandom() % 1000
			if r < 500 && len(alive) > 0 {
				parent := alive[nextRandom()%int64(len(alive))]
				born++
				child := fmt.Sprintf("p%d", born)
				ops = append(ops, op{0, parent, child})
				alive = append(alive, child)
			} else if r < 625 && len(alive) > 0 {
				at := nextRandom() % int64(len(alive))
				name := alive[at]
				alive[at] = alive[len(alive)-1]
				alive = alive[:len(alive)-1]
				ops = append(ops, op{1, name, ""})
			} else if r < 626 {
				ops = append(ops, op{2, "", ""})
			}
		}
		reigns[g] = ops
	}
	var check, names int64
	for _, ops := range reigns {
		t := newThrone("king")
		for _, o := range ops {
			switch o.kind {
			case 0:
				t.birth(o.a, o.b)
			case 1:
				t.death(o.a)
			default:
				order := t.getInheritanceOrder()
				names += int64(len(order))
				for _, name := range order {
					check = (check*31 + int64(len(name)) + 1) % 1000000007
				}
			}
		}
	}
	fmt.Printf("10 reigns of 50000 calls: %d names in the orders, checksum %d\n", names, check)
}
