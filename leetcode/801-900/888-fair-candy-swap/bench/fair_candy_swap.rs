// LeetCode #888 bench: a set of Bob's boxes, on 2000 cases of 5,000 to
// 10^4 boxes each, up to 10^5 candies a box. The same algorithm as
// fair_candy_swap.kara.
use std::collections::HashSet;

fn fair_candy_swap(alice_sizes: &[i64], bob_sizes: &[i64]) -> Vec<i64> {
    let alice_total: i64 = alice_sizes.iter().sum();
    let mut bob_total = 0;
    let mut bob = HashSet::new();
    for &y in bob_sizes {
        bob_total += y;
        bob.insert(y);
    }
    let d = (bob_total - alice_total) / 2;
    let mut best = -1;
    for &x in alice_sizes {
        if bob.contains(&(x + d)) && (best < 0 || x < best) {
            best = x;
        }
    }
    vec![best, best + d]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn below(seed: &mut i64, limit: i64) -> i64 {
    let hi = next_random(seed);
    (hi * 32768 + next_random(seed)) % limit
}

// as in the Kāra bench: Alice's n boxes and Bob's m with a swap that
// evens the totals
fn case_boxes(seed: &mut i64, n: i64, m: i64, most: i64) -> (Vec<i64>, Vec<i64>) {
    loop {
        let mut alice = Vec::new();
        let mut alice_total = 0;
        for _ in 0..n {
            let x = 1 + below(seed, most);
            alice.push(x);
            alice_total += x;
        }
        let mut bob = Vec::new();
        for _ in 0..m {
            bob.push(1 + below(seed, most));
        }
        let i = below(seed, n) as usize;
        let j = below(seed, m) as usize;
        let y = 1 + below(seed, most);
        bob[j] = y;
        let bob_total: i64 = bob.iter().sum();
        let mut short = alice_total + 2 * (y - alice[i]) - bob_total;
        for k in 0..bob.len() {
            if k != j && short != 0 {
                let step = short.max(1 - bob[k]).min(most - bob[k]);
                bob[k] += step;
                short -= step;
            }
        }
        for k in 0..alice.len() {
            if k != i && short != 0 {
                let step = (-short).max(1 - alice[k]).min(most - alice[k]);
                alice[k] += step;
                short += step;
            }
        }
        if short == 0 && y != alice[i] {
            return (alice, bob);
        }
    }
}

fn main() {
    let mut seed = 888;
    let (mut gives, mut takes, mut check) = (0i64, 0i64, 0i64);
    for _ in 0..2000 {
        let n = 5000 + below(&mut seed, 5001);
        let m = 5000 + below(&mut seed, 5001);
        let (alice, bob) = case_boxes(&mut seed, n, m, 100000);
        let swap = fair_candy_swap(&alice, &bob);
        gives += swap[0];
        takes += swap[1];
        check = (check * 131 + swap[0] * 7 + swap[1]) % 1000000007;
    }
    println!("2000 cases of 5000 to 10000 boxes: Alice gives {} candies, Bob {}, checksum {}", gives, takes, check);
}
