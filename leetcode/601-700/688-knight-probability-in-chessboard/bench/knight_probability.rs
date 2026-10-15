// LeetCode #688: Knight Probability in Chessboard -- the chances, forward.
// Bench.
//
// 60 queries, boards of 15 to 25 squares a side and 50 to 100 moves from
// a random start, are drawn once; then 50 rounds answer every query.

const DR: [i64; 8] = [2, 1, -1, -2, -2, -1, 1, 2];
const DC: [i64; 8] = [1, 2, 2, 1, -1, -2, -2, -1];

fn knight_probability(n: i64, k: i64, row: i64, column: i64) -> f64 {
    let mut board = vec![0.0f64; (n * n) as usize];
    board[(row * n + column) as usize] = 1.0;
    for _ in 0..k {
        let mut next = vec![0.0f64; (n * n) as usize];
        for r in 0..n {
            for c in 0..n {
                let p = board[(r * n + c) as usize];
                if p > 0.0 {
                    for m in 0..8 {
                        let r2 = r + DR[m];
                        let c2 = c + DC[m];
                        if r2 >= 0 && r2 < n && c2 >= 0 && c2 < n {
                            next[(r2 * n + c2) as usize] += p / 8.0;
                        }
                    }
                }
            }
        }
        board = next;
    }
    let mut total = 0.0;
    for p in board.iter() {
        total += *p;
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count: i64 = 60;
    let rounds: i64 = 50;
    let mut seed: i64 = 688;
    let mut queries: Vec<(i64, i64, i64, i64)> = Vec::new();
    for _ in 0..count {
        let n = 15 + next_random(&mut seed) % 11;
        let k = 50 + next_random(&mut seed) % 51;
        let row = next_random(&mut seed) % n;
        let column = next_random(&mut seed) % n;
        queries.push((n, k, row, column));
    }
    let mut sum = 0.0;
    for _ in 0..rounds {
        for &(n, k, row, column) in queries.iter() {
            sum += knight_probability(n, k, row, column);
        }
    }
    println!("{} queries answered, sum {:.6}", count * rounds, sum);
}
