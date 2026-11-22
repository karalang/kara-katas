// LeetCode #2836: Maximize Value of Function in a Ball Passing Game --
// the bench, mirrored from ball.kara: binary lifting over 34 levels.

fn get_max_function_value(receiver: &[i64], k: i64) -> i64 {
    let n = receiver.len();
    let levels = 34;
    let mut jump: Vec<Vec<i64>> = vec![receiver.to_vec()];
    let mut gain: Vec<Vec<i64>> = vec![receiver.to_vec()];
    for j in 1..levels {
        let next: Vec<i64> = (0..n).map(|i| jump[j - 1][jump[j - 1][i] as usize]).collect();
        let sum: Vec<i64> =
            (0..n).map(|i| gain[j - 1][i] + gain[j - 1][jump[j - 1][i] as usize]).collect();
        jump.push(next);
        gain.push(sum);
    }
    let mut best = 0;
    for start in 0..n {
        let mut at = start;
        let mut total = start as i64;
        for j in 0..levels {
            if (k >> j) & 1 == 1 {
                total += gain[j][at];
                at = jump[j][at] as usize;
            }
        }
        best = best.max(total);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let count = 10;
    let rounds = 3;
    let n: i64 = 100000;
    let mut seed = 2836;
    let mut games: Vec<(Vec<i64>, i64)> = Vec::new();
    for _ in 0..count {
        let receiver: Vec<i64> = (0..n).map(|_| wide(&mut seed) % n).collect();
        let w = wide(&mut seed);
        let k = (w * 10 + next_random(&mut seed)) % 10000000000 + 1;
        games.push((receiver, k));
    }
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (receiver, k) in games.iter() {
            let best = get_max_function_value(receiver, *k);
            check = (check * 31 + best % 1000000007 + r) % 1000000007;
        }
    }
    println!("{count} games of {n}, {rounds} rounds: checksum {check}");
}
