// LeetCode #1136: Parallel Courses -- the bench, the ★ arm's algorithm:
// Kahn's algorithm a semester at a time.

fn minimum_semesters(n: i64, relations: &Vec<Vec<i64>>) -> i64 {
    let mut after: Vec<Vec<i64>> = vec![Vec::new(); (n + 1) as usize];
    let mut need = vec![0i64; (n + 1) as usize];
    for r in relations.iter() {
        after[r[0] as usize].push(r[1]);
        need[r[1] as usize] += 1;
    }
    let mut now: Vec<i64> = (1..n + 1).filter(|&c| need[c as usize] == 0).collect();
    let mut semesters = 0;
    let mut taken = 0;
    while !now.is_empty() {
        semesters += 1;
        taken += now.len() as i64;
        let mut upcoming: Vec<i64> = Vec::new();
        for &c in now.iter() {
            for &d in after[c as usize].iter() {
                need[d as usize] -= 1;
                if need[d as usize] == 0 {
                    upcoming.push(d);
                }
            }
        }
        now = upcoming;
    }
    if taken == n { semesters } else { -1 }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: i64 = 5000;
    let mut seed: i64 = 1136;
    let mut plans: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..8 {
        let mut relations: Vec<Vec<i64>> = Vec::new();
        for c in 2..n + 1 {
            relations.push(vec![next_random(&mut seed) % (c - 1) + 1, c]);
        }
        plans.push(relations);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..300i64 {
        for j in 0..8i64 {
            let at = ((round * 7919 + j * 104729) % (n - 1)) as usize;
            let c = plans[j as usize][at][1];
            plans[j as usize][at][0] = next_random(&mut seed) % (c - 1) + 1;
            let r = minimum_semesters(n, &plans[j as usize]);
            total += r;
            check = (check * 31 + r + 1) % 1000000007;
        }
    }
    println!("300 rounds over 8 plans of 5000 courses and 4999 relations: semesters total {}, checksum {}", total, check);
}
