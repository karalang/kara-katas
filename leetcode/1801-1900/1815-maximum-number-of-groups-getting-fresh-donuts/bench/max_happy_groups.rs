// LeetCode #1815: Maximum Number of Groups Getting Fresh Donuts -- the
// bench in Rust: the ★ arm over 3000 cases of 30 groups at a batch of 7
// to 9, each group's remainder drawn from the batch's lower half, so that
// no two groups pair off and the search meets the most states.
use std::collections::HashMap;

fn best(b: i64, count: &mut Vec<i64>, left: i64, memo: &mut HashMap<i64, i64>) -> i64 {
    let mut key = 0;
    for r in (1..b).rev() {
        key = key * 31 + count[r as usize];
    }
    if let Some(&known) = memo.get(&key) {
        return known;
    }
    let mut top = 0;
    let mut any = false;
    for r in 1..b {
        if count[r as usize] > 0 {
            any = true;
            count[r as usize] -= 1;
            top = top.max(best(b, count, (left + r) % b, memo));
            count[r as usize] += 1;
        }
    }
    if any && left == 0 {
        top += 1;
    }
    memo.insert(key, top);
    top
}

fn max_happy_groups(batch_size: i64, groups: Vec<i64>) -> i64 {
    let b = batch_size;
    let mut count = vec![0i64; b as usize];
    for g in groups.iter() {
        count[(g % b) as usize] += 1;
    }
    let mut happy = count[0];
    count[0] = 0;
    for r in 1..b {
        let s = b - r;
        if r < s {
            let k = count[r as usize].min(count[s as usize]);
            happy += k;
            count[r as usize] -= k;
            count[s as usize] -= k;
        } else if r == s {
            happy += count[r as usize] / 2;
            count[r as usize] %= 2;
        }
    }
    let mut memo: HashMap<i64, i64> = HashMap::new();
    happy + best(b, &mut count, 0, &mut memo)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1815;
    let mut check: i64 = 0;
    for _ in 0..3000 {
        let b = 7 + next_random(&mut seed) % 3;
        let mut groups: Vec<i64> = Vec::new();
        for _ in 0..30 {
            let whole = next_random(&mut seed) * b;
            groups.push(whole + 1 + next_random(&mut seed) % ((b - 1) / 2));
        }
        check = (check * 31 + max_happy_groups(b, groups)) % 1000000007;
    }
    println!("3000 cases: checksum {}", check);
}
