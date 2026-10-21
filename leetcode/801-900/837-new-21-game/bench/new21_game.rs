// Benchmark for #837: New 21 Game -- the ★ arm (forward, with a sliding window).
//
// Mirrors new21_game.kara: p[i] is the chance that Alice's points are ever
// exactly i, the sum over max_pts of the chances of the totals in the last
// max_pts below i at which she still draws, kept in a running window.

fn new21_game(n: i64, k: i64, max_pts: i64) -> f64 {
    if k == 0 || n >= k - 1 + max_pts {
        return 1.0;
    }
    let w = max_pts as f64;
    let mut p = vec![0.0f64; (n + 1) as usize];
    p[0] = 1.0;
    let mut window = 1.0;
    let mut answer = 0.0;
    for i in 1..n + 1 {
        p[i as usize] = window / w;
        if i < k {
            window += p[i as usize];
        } else {
            answer += p[i as usize];
        }
        let gone = i - max_pts;
        if gone >= 0 && gone < k {
            window -= p[gone as usize];
        }
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 64 games drawn once, each with n from 5000 to 10^4, k from n / 2 to
    // n, and maxPts large enough that Alice can go past n, so that no game
    // takes the early return. Each round plays the next game.
    let count: i64 = 64;
    let rounds: i64 = 25000;
    let mut seed: i64 = 837;
    let mut games: Vec<(i64, i64, i64)> = Vec::new();
    for _ in 0..count {
        let n = 5000 + next_random(&mut seed) % 5001;
        let k = n / 2 + next_random(&mut seed) % (n - n / 2 + 1);
        let least = n - k + 2;
        let max_pts = least + next_random(&mut seed) % (10001 - least);
        games.push((n, k, max_pts));
    }
    let mut sum = 0.0;
    for round in 0..rounds {
        let (n, k, max_pts) = games[(round % count) as usize];
        sum += new21_game(n, k, max_pts);
    }
    println!("{} rounds of {} games: sum {:.6}", rounds, count, sum);
}
