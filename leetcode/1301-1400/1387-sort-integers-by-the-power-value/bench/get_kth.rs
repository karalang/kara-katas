// LeetCode #1387 bench -- Rust: the ★ arm: each value walked only until
// it meets one whose power is known, in a `HashMap` that every walk fills
// on its way back; the (power, value) pairs sorted and the k-th read off.

use std::collections::HashMap;

fn get_kth(lo: i32, hi: i32, k: i32) -> i32 {
    let mut known: HashMap<i64, i32> = HashMap::new();
    known.insert(1, 0);
    let mut keyed: Vec<(i32, i32)> = Vec::new();
    for x in lo..hi + 1 {
        let mut path: Vec<i64> = Vec::new();
        let mut v = x as i64;
        while !known.contains_key(&v) {
            path.push(v);
            v = if v % 2 == 0 { v / 2 } else { 3 * v + 1 };
        }
        let mut steps = known[&v];
        while let Some(p) = path.pop() {
            steps += 1;
            known.insert(p, steps);
        }
        keyed.push((known[&(x as i64)], x));
    }
    keyed.sort();
    keyed[(k - 1) as usize].1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1387;
    let mut check: i64 = 0;
    for _ in 0..4000 {
        seed = (seed + check) % 2147483648;
        let lo = 1 + next_random(&mut seed) % 200;
        let hi = 800 + next_random(&mut seed) % 201;
        let k = 1 + next_random(&mut seed) % (hi - lo + 1);
        check = (check * 131 + get_kth(lo as i32, hi as i32, k as i32) as i64) % 1000000007;
    }
    println!("4000 queries over ranges up to 1 to 1000: checksum {}", check);
}
