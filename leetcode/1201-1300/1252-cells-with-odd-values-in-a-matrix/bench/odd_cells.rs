// LeetCode #1252 bench, in Rust: the ★ arm (the matrix itself, every cell
// of each place's row and column raised by one, then the odd cells
// counted) on 1000 random lists of 100 places in a 50 by 50 matrix built
// once, each asked 40 times; every count folded into a checksum.

fn odd_cells(m: i64, n: i64, indices: &[[i64; 2]]) -> i64 {
    let mut matrix = vec![vec![0i64; n as usize]; m as usize];
    for place in indices {
        let r = place[0] as usize;
        let c = place[1] as usize;
        for j in 0..n as usize {
            matrix[r][j] += 1;
        }
        for i in 0..m as usize {
            matrix[i][c] += 1;
        }
    }
    let mut odd = 0;
    for row in &matrix {
        for &v in row {
            if v % 2 == 1 {
                odd += 1;
            }
        }
    }
    odd
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1252;
    let mut cases: Vec<Vec<[i64; 2]>> = Vec::new();
    for _ in 0..1000 {
        let mut indices = Vec::new();
        for _ in 0..100 {
            let r = next_random(&mut seed) % 50;
            let c = next_random(&mut seed) % 50;
            indices.push([r, c]);
        }
        cases.push(indices);
    }
    let mut check: i64 = 0;
    for _ in 0..40 {
        for indices in &cases {
            check = (check * 131 + odd_cells(50, 50, indices)) % 1000000007;
        }
    }
    println!("40 rounds of 1000 lists of 100 places in 50 by 50: checksum {check}");
}
