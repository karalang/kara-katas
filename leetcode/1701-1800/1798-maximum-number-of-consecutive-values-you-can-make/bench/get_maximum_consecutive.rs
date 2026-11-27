// LeetCode #1798: Maximum Number of Consecutive Values You Can Make -- the
// bench in Rust: the ★ arm over 200 random lists of 2000 coins built once,
// 20000 calls.

fn get_maximum_consecutive(coins: &[i32]) -> i32 {
    let mut sorted = coins.to_vec();
    sorted.sort();
    let mut reach: i32 = 0;
    for &c in sorted.iter() {
        if c > reach + 1 {
            break;
        }
        reach += c;
    }
    reach + 1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1798;
    let mut lists: Vec<Vec<i32>> = Vec::new();
    for _ in 0..200 {
        let coins: Vec<i32> = (0..2000).map(|_| (1 + next_random(&mut seed) % 200) as i32).collect();
        lists.push(coins);
    }
    let mut check: i64 = 0;
    for call in 0..20000i64 {
        let coins = &lists[((check + call) % 200) as usize];
        check = (check * 31 + get_maximum_consecutive(coins) as i64) % 1000000007;
    }
    println!("20000 calls over 200 lists of 2000 coins: checksum {}", check);
}
