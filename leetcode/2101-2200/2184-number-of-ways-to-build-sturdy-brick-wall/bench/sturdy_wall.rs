// LeetCode #2184: Number of Ways to Build Sturdy Brick Wall -- the
// benchmark's Rust mirror of sturdy_wall.kara.

fn fill(at: i64, joints: i64, width: i64, bricks: &[i64], rows: &mut Vec<i64>) {
    if at == width {
        rows.push(joints);
        return;
    }
    for &b in bricks {
        let end = at + b;
        if end < width {
            fill(end, joints | (1 << end), width, bricks, rows);
        } else if end == width {
            fill(end, joints, width, bricks, rows);
        }
    }
}

fn build_wall(height: i64, width: i64, bricks: &[i64]) -> i64 {
    let mut rows: Vec<i64> = Vec::new();
    fill(0, 0, width, bricks, &mut rows);
    let n = rows.len();
    let mut fits: Vec<Vec<usize>> = Vec::new();
    for a in 0..n {
        let mut on: Vec<usize> = Vec::new();
        for b in 0..n {
            if rows[a] & rows[b] == 0 {
                on.push(b);
            }
        }
        fits.push(on);
    }
    let mut ways: Vec<i64> = vec![1; n];
    for _ in 1..height {
        let mut next: Vec<i64> = vec![0; n];
        for a in 0..n {
            for &b in &fits[a] {
                next[b] = (next[b] + ways[a]) % 1000000007;
            }
        }
        ways = next;
    }
    let mut total = 0;
    for &w in &ways {
        total = (total + w) % 1000000007;
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2184i64;
    let mut check = 0i64;
    for _ in 0..1000 {
        let height = next_random(&mut seed) % 51 + 50;
        let mut bricks: Vec<i64> = vec![1];
        for b in 2..11 {
            if next_random(&mut seed) % 2 == 0 {
                bricks.push(b);
            }
        }
        check = (check * 31 + build_wall(height, 10, &bricks)) % 1000000007;
    }
    println!("1000 walls: checksum {}", check);
}
