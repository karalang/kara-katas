// LeetCode #2491: Divide Players Into Teams of Equal Skill -- Rust mirror
// of the ★ arm's benchmark (divide.kara): the same 20 lists and 25
// passes, each list cloned and sorted for every answer.

fn divide_players(skill: &[i64]) -> i64 {
    let mut sorted = skill.to_vec();
    sorted.sort();
    let n = sorted.len();
    let target = sorted[0] + sorted[n - 1];
    let mut chemistry = 0;
    for i in 0..n / 2 {
        let (a, b) = (sorted[i], sorted[n - 1 - i]);
        if a + b != target {
            return -1;
        }
        chemistry += a * b;
    }
    chemistry
}

fn main() {
    let n: i64 = 100000;
    let passes: i64 = 25;
    let mut seed: i64 = 2491;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for l in 0..20 {
        let total = 500 + l * 50;
        let mut skill: Vec<i64> = Vec::new();
        for _ in 0..n / 2 {
            let a = next_random() % (total - 1) + 1;
            skill.push(a);
            skill.push(total - a);
        }
        for i in (1..n).rev() {
            let hi = next_random();
            let j = (hi * 32768 + next_random()) % (i + 1);
            skill.swap(i as usize, j as usize);
        }
        lists.push(skill);
    }
    let mut check: i64 = 0;
    for p in 0..passes {
        for l in 0..20 {
            let at = (check % n) as usize;
            let was = lists[l][at];
            lists[l][at] = (check / n + p) % 1000 + 1;
            check = (check * 31 + divide_players(&lists[l]) + 1 + p) % 1_000_000_007;
            lists[l][at] = was;
        }
    }
    println!("{} passes over 20 lists of 10^5: checksum {}", passes, check);
}
