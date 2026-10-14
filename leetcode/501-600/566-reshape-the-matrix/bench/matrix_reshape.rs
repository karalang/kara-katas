// Benchmark for #566: Rust mirror of the ★ arm (index arithmetic); see
// matrix_reshape.kara.

fn matrix_reshape(mat: &[Vec<i64>], r: i64, c: i64) -> Vec<Vec<i64>> {
    let m = mat.len() as i64;
    let n = mat[0].len() as i64;
    if m * n != r * c {
        return mat.to_vec();
    }
    let mut out: Vec<Vec<i64>> = Vec::new();
    for i in 0..r {
        let mut row: Vec<i64> = Vec::new();
        for j in 0..c {
            let k = i * c + j;
            row.push(mat[(k / n) as usize][(k % n) as usize]);
        }
        out.push(row);
    }
    out
}

// ---- benchmark --------------------------------------------------------------

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count: i64 = 20;
    let rounds: i64 = 800;
    let shapes: [(i64, i64); 10] =
        [(1, 10000), (4, 2500), (25, 400), (50, 200), (100, 100), (200, 50), (400, 25), (2500, 4), (10000, 1), (99, 101)];
    let mut seed: i64 = 566;
    let mut mats: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..count {
        let mut mat: Vec<Vec<i64>> = Vec::new();
        for _ in 0..100 {
            let mut row: Vec<i64> = Vec::new();
            for _ in 0..100 {
                row.push(step(&mut seed) % 2001 - 1000);
            }
            mat.push(row);
        }
        mats.push(mat);
    }
    let mut cells: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for g in 0..count {
            let (r, c) = shapes[((round + g) % 10) as usize];
            let got = matrix_reshape(&mats[((round * 7 + g) % count) as usize], r, c);
            let rows = got.len() as i64;
            let cols = got[0].len() as i64;
            cells += rows * cols;
            checksum = (checksum * 31 + got[(round % rows) as usize][(g % cols) as usize] + 1000) % 1000000007;
        }
    }
    println!("{} matrices of 100 by 100, {} rounds: {} cells, checksum {}", count, rounds, cells, checksum);
}
