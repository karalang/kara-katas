// LeetCode #1125: Smallest Sufficient Team -- the bench in Go: the ★ arm (a
// `map[string]int` from skill to bit, `team[m]` a slice for each mask, nil
// until reached) over the same 8 problems and 8 rounds.
package main

import "fmt"

func smallestSufficientTeam(reqSkills []string, people [][]string) []int64 {
	bit := make(map[string]int)
	for i, s := range reqSkills {
		bit[s] = i
	}
	full := (1 << len(reqSkills)) - 1
	team := make([][]int64, full+1)
	reached := make([]bool, full+1)
	team[0] = []int64{}
	reached[0] = true
	for p, skills := range people {
		mask := 0
		for _, s := range skills {
			mask |= 1 << bit[s]
		}
		if mask == 0 {
			continue
		}
		for m := 0; m <= full; m++ {
			grown := m | mask
			if grown == m || !reached[m] {
				continue
			}
			if !reached[grown] || len(team[m])+1 < len(team[grown]) {
				next := make([]int64, len(team[m]), len(team[m])+1)
				copy(next, team[m])
				team[grown] = append(next, int64(p))
				reached[grown] = true
			}
		}
	}
	return team[full]
}

var seed int64 = 1125

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
	req := make([]string, 16)
	for i := range req {
		req[i] = fmt.Sprintf("s%d", i)
	}
	problems := make([][][]string, 0, 8)
	for j := 0; j < 8; j++ {
		people := make([][]string, 0, 60)
		for i := 0; i < 60; i++ {
			skills := []string{}
			for _, s := range req {
				if nextRandom()%100 < 20 {
					skills = append(skills, s)
				}
			}
			people = append(people, skills)
		}
		problems = append(problems, people)
	}
	var total, check int64
	for round := int64(0); round < 8; round++ {
		for _, people := range problems {
			who := int(nextRandom() % 60)
			skill := fmt.Sprintf("s%d", nextRandom()%16)
			at := -1
			for i, s := range people[who] {
				if s == skill {
					at = i
					break
				}
			}
			if at >= 0 {
				people[who] = append(people[who][:at], people[who][at+1:]...)
			} else {
				people[who] = append(people[who], skill)
			}
			for _, s := range req {
				found := false
				for _, p := range people {
					if contains(p, s) {
						found = true
						break
					}
				}
				if !found {
					people[(who+1)%60] = append(people[(who+1)%60], s)
				}
			}
			team := smallestSufficientTeam(req, people)
			total += int64(len(team))
			for _, p := range team {
				check = (check*61 + p + 1) % 1000000007
			}
			check = (check*17 + round) % 1000000007
		}
	}
	fmt.Printf("8 rounds over 8 problems of 16 skills and 60 people: team sizes total %d, checksum %d\n", total, check)
}
