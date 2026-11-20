// LeetCode #1217: Minimum Cost to Move Chips to The Same Position -- the
// bench in Rust: the ★ arm (the odd and the even chips counted, the
// lesser count the cost) on the same 20000 sets of 100 chips and 20
// rounds.

fn min_cost_to_move_chips(position: &[i64]) -> i64 {
    let mut odd = 0;
    let mut even = 0;
    for &p in position.iter() {
        if p % 2 == 1 {
            odd += 1;
        } else {
            even += 1;
        }
    }
    odd.min(even)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1217;
    let mut sets: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20000 {
        let mut chips = Vec::with_capacity(100);
        for _ in 0..100 {
            let hi = next_random(&mut seed);
            let lo = next_random(&mut seed);
            chips.push((hi * 32768 + lo) % 1000000000 + 1);
        }
        sets.push(chips);
    }
    let mut check: i64 = 0;
    for round in 0..20 {
        for chips in sets.iter() {
            check = (check * 131 + min_cost_to_move_chips(chips) + round) % 1000000007;
        }
    }
    println!("20 rounds over 20000 sets of 100 chips: checksum {}", check);
}
