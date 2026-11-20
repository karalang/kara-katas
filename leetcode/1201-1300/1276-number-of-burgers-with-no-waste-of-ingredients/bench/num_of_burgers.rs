// LeetCode #1276 bench, in Rust: the ★ arm (by algebra) on 100,000 random
// pairs of tomato and cheese slice counts up to 10^7, a third made from
// burgers and a third near such a count, drawn once; 1000 rounds, every
// answer folded into a checksum.

fn num_of_burgers(tomato_slices: i64, cheese_slices: i64) -> Vec<i64> {
    if tomato_slices % 2 != 0 {
        return Vec::new();
    }
    let jumbo = tomato_slices / 2 - cheese_slices;
    let small = 2 * cheese_slices - tomato_slices / 2;
    if jumbo < 0 || small < 0 {
        return Vec::new();
    }
    vec![jumbo, small]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1276i64;
    let mut cases: Vec<(i64, i64)> = Vec::new();
    for case in 0..100000 {
        let jumbo = next_random(&mut seed) % 2500000;
        let small = next_random(&mut seed) % 2500000;
        let (t, c) = if case % 3 == 0 {
            (4 * jumbo + 2 * small, jumbo + small)
        } else if case % 3 == 1 {
            let t = 4 * jumbo + 2 * small + next_random(&mut seed) % 5 - 2;
            (t, jumbo + small + next_random(&mut seed) % 3 - 1)
        } else {
            let t = next_random(&mut seed) % 10000001;
            (t, next_random(&mut seed) % 5000001)
        };
        cases.push((t.max(0), c.max(0)));
    }
    let mut check = 0i64;
    for round in 0..1000 {
        for &(t, c) in cases.iter() {
            let answer = num_of_burgers(t + round, c);
            check = if answer.len() == 2 {
                (check * 131 + answer[0] * 7 + answer[1]) % 1000000007
            } else {
                (check * 131 + 1) % 1000000007
            };
        }
    }
    println!("1000 rounds of 100000 pairs: checksum {}", check);
}
