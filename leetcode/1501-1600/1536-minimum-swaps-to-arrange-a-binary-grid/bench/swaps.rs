// LeetCode #1536: Minimum Swaps to Arrange a Binary Grid -- bench: the ★
// arm over 50 random 200 x 200 grids, built once and answered 50 times.
// Rust mirror of swaps.kara.

fn min_swaps(grid: &[Vec<i64>]) -> i64 {
    let n = grid.len();
    let mut zeros: Vec<usize> = Vec::new();
    for row in grid {
        let mut count = 0;
        while count < n && row[n - 1 - count] == 0 {
            count += 1;
        }
        zeros.push(count);
    }
    let mut swaps = 0i64;
    for i in 0..n {
        let need = n - 1 - i;
        let mut j = i;
        while j < n && zeros[j] < need {
            j += 1;
        }
        if j == n {
            return -1;
        }
        while j > i {
            zeros.swap(j, j - 1);
            j -= 1;
            swaps += 1;
        }
    }
    swaps
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn grid(n: i64, seed: &mut i64) -> Vec<Vec<i64>> {
    let mut zeros: Vec<i64> = (0..n).collect();
    if next_random(seed) % 2 == 0 {
        for i in (1..n).rev() {
            let j = next_random(seed) % (i + 1);
            zeros.swap(i as usize, j as usize);
        }
        for i in 0..n as usize {
            zeros[i] = (zeros[i] + next_random(seed) % 2).min(n);
        }
    } else {
        for i in 0..n as usize {
            zeros[i] = next_random(seed) % (n + 1);
        }
    }
    let mut rows = Vec::new();
    for i in 0..n as usize {
        let mut row = vec![0i64; n as usize];
        if zeros[i] < n {
            row[(n - 1 - zeros[i]) as usize] = 1;
            for c in 0..(n - 1 - zeros[i]) as usize {
                row[c] = next_random(seed) % 2;
            }
        }
        rows.push(row);
    }
    rows
}

fn main() {
    let mut seed = 1536i64;
    let grids: Vec<Vec<Vec<i64>>> = (0..50).map(|_| grid(200, &mut seed)).collect();
    let mut check = 0;
    for _ in 0..50 {
        for g in &grids {
            check = mix(check, min_swaps(g) + 1);
        }
    }
    println!("50 passes over 50 grids of 200 rows: checksum {}", check);
}
