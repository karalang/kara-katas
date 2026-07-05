// Bench mirror of spiral_bench.kara — boundary-shrinking spiral over a batch of LCG-filled
// 24×24 matrices, position-weighted checksum folded into an i64 sink. rustc -O.
// See ../README.md § Benchmarks.

fn main() {
    let m: i64 = 1103515245; // glibc LCG multiplier
    let inc: i64 = 12345; // glibc LCG increment
    let modulus: i64 = 2147483648; // 2^31
    let windows: i64 = 200000; // number of simulated input matrices
    let rows: i64 = 24;
    let cols: i64 = 24;
    let n: i64 = 576; // rows * cols

    let mut grid = [0i64; 576];
    let mut state: i64 = 1; // LCG seed
    let mut sink: i64 = 0;
    let mut k: i64 = 0;
    while k < windows {
        let mut idx = 0i64;
        while idx < n {
            state = (state * m + inc) % modulus;
            grid[idx as usize] = (state % 100) - 50;
            idx += 1;
        }
        let mut local = 0i64;
        let mut pos = 0i64;
        let mut top = 0i64;
        let mut bottom = rows - 1;
        let mut left = 0i64;
        let mut right = cols - 1;
        while top <= bottom && left <= right {
            let mut c = left;
            while c <= right {
                local += (pos + 1) * grid[(top * cols + c) as usize];
                pos += 1;
                c += 1;
            }
            top += 1;
            let mut r = top;
            while r <= bottom {
                local += (pos + 1) * grid[(r * cols + right) as usize];
                pos += 1;
                r += 1;
            }
            right -= 1;
            if top <= bottom {
                let mut c2 = right;
                while c2 >= left {
                    local += (pos + 1) * grid[(bottom * cols + c2) as usize];
                    pos += 1;
                    c2 -= 1;
                }
                bottom -= 1;
            }
            if left <= right {
                let mut r2 = bottom;
                while r2 >= top {
                    local += (pos + 1) * grid[(r2 * cols + left) as usize];
                    pos += 1;
                    r2 -= 1;
                }
                left += 1;
            }
        }
        sink += local;
        k += 1;
    }
    println!("{}", sink);
}
