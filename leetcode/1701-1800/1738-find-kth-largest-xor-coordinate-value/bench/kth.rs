// LeetCode #1738: Find Kth Largest XOR Coordinate Value -- the bench
// (kth.kara): a prefix XOR table, then a sort.

fn kth_largest_value(matrix: &[Vec<i32>], k: i32) -> i32 {
    let (m, n) = (matrix.len(), matrix[0].len());
    let mut prefix: Vec<Vec<i32>> = vec![vec![0; n + 1]; m + 1];
    let mut values: Vec<i32> = Vec::with_capacity(m * n);
    for i in 0..m {
        for j in 0..n {
            prefix[i + 1][j + 1] =
                prefix[i][j + 1] ^ prefix[i + 1][j] ^ prefix[i][j] ^ matrix[i][j];
            values.push(prefix[i + 1][j + 1]);
        }
    }
    values.sort();
    values[values.len() - k as usize]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let count = 4;
    let rounds: i64 = 5;
    let side: i64 = 1000;
    let mut seed: i64 = 1738;
    let mut problems: Vec<(Vec<Vec<i32>>, i32)> = Vec::new();
    for _ in 0..count {
        let mut matrix: Vec<Vec<i32>> = Vec::new();
        for _ in 0..side {
            matrix.push(
                (0..side)
                    .map(|_| (wide(&mut seed) % 1000001) as i32)
                    .collect(),
            );
        }
        let k = (wide(&mut seed) % (side * side) + 1) as i32;
        problems.push((matrix, k));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (matrix, k) in problems.iter() {
            let answer = kth_largest_value(matrix, *k) as i64;
            sum += answer;
            check = (check * 31 + answer + *k as i64 + r) % 1000000007;
        }
    }
    println!(
        "{} matrices of {} by {}, {} rounds: answers sum to {}, checksum {}",
        count, side, side, rounds, sum, check
    );
}
