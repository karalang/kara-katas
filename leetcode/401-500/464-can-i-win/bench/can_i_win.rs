// Benchmark for #464: mirror of can_i_win.kara (the ★ arm: search with a
// memo keyed by the bitmask of numbers used) on the same workload. The
// memo is the standard library's HashMap.
use std::collections::HashMap;

fn wins_from(used: i64, left: i64, m: i64, memo: &mut HashMap<i64, bool>) -> bool {
    if let Some(&known) = memo.get(&used) {
        return known;
    }
    let mut result = false;
    for n in 1..m + 1 {
        let bit = 1 << (n - 1);
        if used & bit == 0 && (n >= left || !wins_from(used | bit, left - n, m, memo)) {
            result = true;
            break;
        }
    }
    memo.insert(used, result);
    result
}

fn can_i_win(max_choosable: i64, desired_total: i64) -> bool {
    if desired_total <= 0 {
        return true;
    }
    if max_choosable * (max_choosable + 1) / 2 < desired_total {
        return false;
    }
    let mut memo: HashMap<i64, bool> = HashMap::new();
    wins_from(0, desired_total, max_choosable, &mut memo)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let games = 10;
    let mut seed: i64 = 464;
    let mut won = 0;
    let mut checksum: i64 = 0;
    for game in 0..games {
        let total = 100 + next_random(&mut seed) % 111;
        if can_i_win(20, total) {
            won += 1;
            checksum = (checksum * 31 + game + 1) % 1000000007;
        }
    }
    println!("{} games of 1 to 20: the first player wins {}, checksum {}", games, won, checksum);
}
