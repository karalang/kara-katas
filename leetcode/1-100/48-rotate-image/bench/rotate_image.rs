// LeetCode #48 bench mirror — Rust, the in-place layer four-way cyclic rotation (★).
//
// Mirrors bench/rotate_image.kara: rotate a fixed n=20 matrix 90° clockwise IN PLACE by cycling
// four cells at a time, TOTAL times with the state carrying forward; one cell punched per iteration
// (`m[k%n][(k*7)%n] = k%97`), folding a position-weighted per-cell signature into a rolling
// checksum. Kāra writes the four-cell cycle as a single four-target parallel assignment; Rust's
// borrow checker forbids four simultaneous `&mut` into the same Vec, so the identical rotation is
// expressed with one temporary (top saved, then top←left←bottom←right←top). Prints the same sink.

fn rotate(m: &mut [Vec<i64>]) {
    let n = m.len();
    for i in 0..n / 2 {
        for j in i..n - 1 - i {
            let tmp = m[i][j];
            m[i][j] = m[n - 1 - j][i];
            m[n - 1 - j][i] = m[n - 1 - i][n - 1 - j];
            m[n - 1 - i][n - 1 - j] = m[j][n - 1 - i];
            m[j][n - 1 - i] = tmp;
        }
    }
}

fn main() {
    let total: i64 = 40000;
    let modulus: i64 = 1000000007;
    let n: usize = 20;

    let mut m: Vec<Vec<i64>> = (0..n)
        .map(|a| (0..n).map(|b| ((a * 7 + b * 13) % 97) as i64).collect())
        .collect();

    let mut acc: i64 = 0;
    for k in 0..total {
        let kk = k as usize;
        m[kk % n][(kk * 7) % n] = k % 97;
        rotate(&mut m);

        let mut sig: i64 = 0;
        for i in 0..n {
            let row = &m[i];
            for j in 0..n {
                sig = (sig * 31 + row[j] * ((i * n + j + 1) as i64)) % modulus;
            }
        }
        acc = (acc * 131 + sig) % modulus;
    }

    println!("{}", acc);
}
