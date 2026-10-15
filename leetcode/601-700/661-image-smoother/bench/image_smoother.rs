// Benchmark for #661: each cell's 3x3 window, as the Kara ★ arm.

fn image_smoother(img: &[Vec<i64>]) -> Vec<Vec<i64>> {
    let m = img.len();
    let n = img[0].len();
    let mut out = Vec::with_capacity(m);
    for i in 0..m {
        let mut row = Vec::with_capacity(n);
        for j in 0..n {
            let mut sum = 0i64;
            let mut count = 0i64;
            for r in i.saturating_sub(1)..(i + 2).min(m) {
                for c in j.saturating_sub(1)..(j + 2).min(n) {
                    sum += img[r][c];
                    count += 1;
                }
            }
            row.push(sum / count);
        }
        out.push(row);
    }
    out
}

fn main() {
    let size = 1000usize;
    let passes = 20;
    let mut seed: i64 = 661;
    let mut next_random = move || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut img: Vec<Vec<i64>> = Vec::new();
    for _ in 0..size {
        let mut row = Vec::with_capacity(size);
        for _ in 0..size {
            row.push(next_random() % 256);
        }
        img.push(row);
    }
    for _ in 0..passes {
        img = image_smoother(&img);
    }
    let mut checksum: i64 = 0;
    for row in &img {
        for &v in row {
            checksum = (checksum * 31 + v) % 1000000007;
        }
    }
    println!("{}x{}, {} passes: checksum {}", size, size, passes, checksum);
}
