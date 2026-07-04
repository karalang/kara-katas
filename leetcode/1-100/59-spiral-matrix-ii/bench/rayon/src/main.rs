// LeetCode #59 — rayon-parallel Rust mirror (par lane, spiral_matrix_ii).
// Same boundary-shrinking generator + position-weighted checksum as
// ../spiral_matrix_ii.rs; the K=180k reduction runs across a rayon pool.
// Hand-tuned-parallel comparator for Kāra's auto-par. Sink matches the
// kara/rust/c/go mirrors.

fn generate_matrix(n: i64) -> Vec<Vec<i64>> {
    let un = n as usize;
    let mut grid: Vec<Vec<i64>> = (0..un).map(|_| vec![0i64; un]).collect();

    let mut top = 0i64;
    let mut bottom = n - 1;
    let mut left = 0i64;
    let mut right = n - 1;
    let mut v = 1i64;

    while top <= bottom && left <= right {
        let mut c = left;
        while c <= right {
            grid[top as usize][c as usize] = v;
            v += 1;
            c += 1;
        }
        top += 1;

        let mut r2 = top;
        while r2 <= bottom {
            grid[r2 as usize][right as usize] = v;
            v += 1;
            r2 += 1;
        }
        right -= 1;

        if top <= bottom {
            let mut c2 = right;
            while c2 >= left {
                grid[bottom as usize][c2 as usize] = v;
                v += 1;
                c2 -= 1;
            }
            bottom -= 1;
        }

        if left <= right {
            let mut r3 = bottom;
            while r3 >= top {
                grid[r3 as usize][left as usize] = v;
                v += 1;
                r3 -= 1;
            }
            left += 1;
        }
    }
    grid
}

fn checksum(grid: &[Vec<i64>], n: i64) -> i64 {
    let mut s = 0i64;
    for i in 0..n {
        for j in 0..n {
            s += grid[i as usize][j as usize] * (i * n + j + 1);
        }
    }
    s
}

fn main() {
    use rayon::prelude::*;
    let m_sizes: i64 = 9;
    let k_iters: i64 = 180_000;

    let total: i64 = (0..k_iters)
        .into_par_iter()
        .map(|k| {
            let n = 12 + (k % m_sizes);
            let g = generate_matrix(n);
            checksum(&g, n)
        })
        .sum();
    println!("{}", total);
}
