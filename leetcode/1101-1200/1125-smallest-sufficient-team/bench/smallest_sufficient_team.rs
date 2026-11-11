// LeetCode #1125: Smallest Sufficient Team -- the bench in Rust: the ★ arm
// (a `HashMap` from skill to bit, `team[m]` an `Option<Vec<i64>>` for each
// mask) over the same 8 problems and 8 rounds.
use std::collections::HashMap;

fn smallest_sufficient_team(req_skills: &[String], people: &[Vec<String>]) -> Vec<i64> {
    let mut bit: HashMap<String, i64> = HashMap::new();
    for (i, s) in req_skills.iter().enumerate() {
        bit.insert(s.clone(), i as i64);
    }
    let full = (1usize << req_skills.len()) - 1;
    let mut team: Vec<Option<Vec<i64>>> = vec![None; full + 1];
    team[0] = Some(Vec::new());
    for (p, skills) in people.iter().enumerate() {
        let mut mask = 0usize;
        for s in skills {
            mask |= 1 << bit[s];
        }
        if mask == 0 {
            continue;
        }
        for m in 0..full + 1 {
            let grown = m | mask;
            if grown == m {
                continue;
            }
            if let Some(t) = &team[m] {
                let better = match &team[grown] {
                    Some(g) => t.len() + 1 < g.len(),
                    None => true,
                };
                if better {
                    let mut next = t.clone();
                    next.push(p as i64);
                    team[grown] = Some(next);
                }
            }
        }
    }
    team[full].take().unwrap()
}

static mut SEED: i64 = 1125;

fn next_random() -> i64 {
    unsafe {
        SEED = (SEED * 1103515245 + 12345) % 2147483648;
        SEED / 65536
    }
}

fn main() {
    let req: Vec<String> = (0..16).map(|i| format!("s{i}")).collect();
    let mut problems: Vec<Vec<Vec<String>>> = Vec::new();
    for _ in 0..8 {
        let mut people: Vec<Vec<String>> = Vec::new();
        for _ in 0..60 {
            let mut skills: Vec<String> = Vec::new();
            for s in &req {
                if next_random() % 100 < 20 {
                    skills.push(s.clone());
                }
            }
            people.push(skills);
        }
        problems.push(people);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..8i64 {
        for people in problems.iter_mut() {
            let who = (next_random() % 60) as usize;
            let skill = format!("s{}", next_random() % 16);
            if let Some(at) = people[who].iter().position(|s| *s == skill) {
                people[who].remove(at);
            } else {
                people[who].push(skill);
            }
            for s in &req {
                if !people.iter().any(|p| p.contains(s)) {
                    people[(who + 1) % 60].push(s.clone());
                }
            }
            let team = smallest_sufficient_team(&req, people);
            total += team.len() as i64;
            for p in &team {
                check = (check * 61 + p + 1) % 1000000007;
            }
            check = (check * 17 + round) % 1000000007;
        }
    }
    println!("8 rounds over 8 problems of 16 skills and 60 people: team sizes total {total}, checksum {check}");
}
