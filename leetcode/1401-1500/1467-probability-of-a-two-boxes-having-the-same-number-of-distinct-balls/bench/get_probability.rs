// LeetCode #1467 bench in Rust: the ★ arm (a depth-first search over how
// many of each colour go into the first box) on the same 100 sets of 8
// colours and 2 passes.

fn choose(n: i64, k: i64) -> i64 {
    let mut c = 1;
    for i in 0..k {
        c = c * (n - i) / (i + 1);
    }
    c
}

fn ways(balls: &[i32], i: usize, first: i64, a: i64, b: i64) -> i64 {
    if i == balls.len() {
        return if first == 0 && a == b { 1 } else { 0 };
    }
    let n = balls[i] as i64;
    let mut total = 0;
    for j in 0..=n.min(first) {
        let a2 = if j > 0 { a + 1 } else { a };
        let b2 = if j < n { b + 1 } else { b };
        total += choose(n, j) * ways(balls, i + 1, first - j, a2, b2);
    }
    total
}

fn get_probability(balls: &[i32]) -> f64 {
    let total = balls.iter().sum::<i32>() as i64;
    let good = ways(balls, 0, total / 2, 0, 0);
    good as f64 / choose(total, total / 2) as f64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1467i64;
    let mut sets: Vec<Vec<i32>> = Vec::new();
    while sets.len() < 100 {
        let balls: Vec<i32> = (0..8).map(|_| (1 + next_random(&mut seed) % 6) as i32).collect();
        if balls.iter().sum::<i32>() % 2 == 0 {
            sets.push(balls);
        }
    }
    let mut check: i64 = 0;
    for pass in 0..2 {
        for s in 0..100 {
            let k = (check % 8) as usize;
            sets[s][k] = if sets[s][k] <= 4 { sets[s][k] + 2 } else { sets[s][k] - 2 };
            let p = get_probability(&sets[s]);
            check = (check * 31 + (p * 1000000000.0 + 0.5).floor() as i64 + pass) % 1000000007;
        }
    }
    println!("2 passes over 100 sets of 8 colours: checksum {check}");
}
