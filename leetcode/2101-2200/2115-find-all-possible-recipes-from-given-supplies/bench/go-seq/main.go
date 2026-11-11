// LeetCode #2115: Find All Possible Recipes from Given Supplies -- the
// benchmark, the same algorithm as recipes.kara: Kahn's order over names,
// a map from each ingredient to the recipes needing it and a queue
// starting with the supplies.

package main

import "fmt"

func findAllRecipes(recipes []string, ingredients [][]string, supplies []string) []string {
	neededBy := map[string][]int{}
	lacking := []int{}
	for i := range recipes {
		lacking = append(lacking, len(ingredients[i]))
		for _, item := range ingredients[i] {
			neededBy[item] = append(neededBy[item], i)
		}
	}
	queue := append([]string{}, supplies...)
	made := []string{}
	for head := 0; head < len(queue); head++ {
		item := queue[head]
		if users, ok := neededBy[item]; ok {
			for _, i := range users {
				lacking[i]--
				if lacking[i] == 0 {
					made = append(made, recipes[i])
					queue = append(queue, recipes[i])
				}
			}
		}
	}
	return made
}

var seed int64 = 2115

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func contains(list []string, s string) bool {
	for _, x := range list {
		if x == s {
			return true
		}
	}
	return false
}

func main() {
	recipes := make([]string, 100)
	for i := range recipes {
		recipes[i] = fmt.Sprintf("r%d", i)
	}
	supplies := make([]string, 56)
	for i := range supplies {
		supplies[i] = fmt.Sprintf("s%d", i)
	}
	kitchens := make([][][]string, 40)
	for k := range kitchens {
		ingredients := make([][]string, 100)
		for i := int64(0); i < 100; i++ {
			need := []string{}
			count := nextRandom()%8 + 1
			for c := int64(0); c < count; c++ {
				pick := nextRandom() % (60 + i)
				var item string
				if pick < 60 {
					item = fmt.Sprintf("s%d", pick)
				} else {
					item = fmt.Sprintf("r%d", pick-60)
				}
				if !contains(need, item) {
					need = append(need, item)
				}
			}
			if len(need) == 0 {
				need = append(need, "s0")
			}
			ingredients[i] = need
		}
		kitchens[k] = ingredients
	}
	var total, check int64
	for round := 0; round < 10; round++ {
		for k := 0; k < 40; k++ {
			i := (round*37 + k) % 100
			kitchens[k][i][0] = fmt.Sprintf("s%d", (round+k)%50)
			got := findAllRecipes(recipes, kitchens[k], supplies)
			total += int64(len(got))
			check = (check*31 + int64(len(got))) % 1000000007
		}
	}
	fmt.Printf("400 solves: %d recipes made, checksum %d\n", total, check)
}
