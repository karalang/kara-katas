// LeetCode #2768: Number of Black Blocks -- the bench in Rust: the ★ arm
// over 100 grids of 10^4 black cells, all drawn first, then each answered
// 5 times. The blocks in a `HashMap` keyed by the top-left corner.

use std::collections::HashMap;

fn count_black_blocks(m: i64, n: i64, coordinates: &Vec<Vec<i64>>) -> Vec<i64> {
    let mut blocks: HashMap<(i64, i64), i64> = HashMap::new();
    for cell in coordinates.iter() {
        let (x, y) = (cell[0], cell[1]);
        for bx in (x - 1).max(0)..=x.min(m - 2) {
            for by in (y - 1).max(0)..=y.min(n - 2) {
                *blocks.entry((bx, by)).or_insert(0) += 1;
            }
        }
    }
    let mut counts = vec![0i64; 5];
    for (_, &black) in blocks.iter() {
        counts[black as usize] += 1;
    }
    counts[0] = (m - 1) * (n - 1) - blocks.len() as i64;
    counts
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn gcd(a: i64, b: i64) -> i64 {
    if b == 0 { a } else { gcd(b, a % b) }
}

fn main() {
    let count = 100;
    let rounds = 5;
    let mut seed: i64 = 2768;
    let mut grids: Vec<(i64, i64, Vec<Vec<i64>>)> = Vec::new();
    for _ in 0..count {
        let side = wide(&mut seed) % 900 + 101;
        let area = side * side;
        let m = side + wide(&mut seed) % (100001 - side);
        let n = side + wide(&mut seed) % (100001 - side);
        let x0 = wide(&mut seed) % (m - side + 1);
        let y0 = wide(&mut seed) % (n - side + 1);
        let mut stride = wide(&mut seed) % area;
        while gcd(stride, area) != 1 {
            stride = wide(&mut seed) % area;
        }
        let start = wide(&mut seed) % area;
        let cells: Vec<Vec<i64>> = (0..10000i64)
            .map(|k| {
                let at = (start + k * stride) % area;
                vec![x0 + at / side, y0 + at % side]
            })
            .collect();
        grids.push((m, n, cells));
    }
    let mut sums = vec![0i64; 5];
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (m, n, cells) in grids.iter() {
            let counts = count_black_blocks(*m, *n, cells);
            for i in 0..5 {
                sums[i] += counts[i];
                check = (check * 31 + counts[i] % 1000000007 + r + 1) % 1000000007;
            }
        }
    }
    println!("{} grids of 10^4 cells, {} rounds: counts sum to {:?}, checksum {}", count, rounds, sums, check);
}
