// LeetCode #2132: Stamping the Grid -- the benchmark, the same algorithm
// as stamp.kara.

fn possible_to_stamp(grid: &[Vec<i64>], stamp_height: i64, stamp_width: i64) -> bool {
    let m = grid.len() as i64;
    let n = grid[0].len() as i64;
    let w = n + 1;
    let mut full = vec![0i64; ((m + 1) * w) as usize];
    for r in 0..m {
        for c in 0..n {
            full[((r + 1) * w + c + 1) as usize] = grid[r as usize][c as usize]
                + full[(r * w + c + 1) as usize]
                + full[((r + 1) * w + c) as usize]
                - full[(r * w + c) as usize];
        }
    }
    let mut marks = vec![0i64; ((m + 1) * w) as usize];
    for r in 0..m - stamp_height + 1 {
        for c in 0..n - stamp_width + 1 {
            let r2 = r + stamp_height;
            let c2 = c + stamp_width;
            if full[(r2 * w + c2) as usize] - full[(r * w + c2) as usize] - full[(r2 * w + c) as usize]
                + full[(r * w + c) as usize]
                == 0
            {
                marks[(r * w + c) as usize] += 1;
                marks[(r * w + c2) as usize] -= 1;
                marks[(r2 * w + c) as usize] -= 1;
                marks[(r2 * w + c2) as usize] += 1;
            }
        }
    }
    for r in 0..m {
        for c in 0..n {
            if r > 0 {
                marks[(r * w + c) as usize] += marks[((r - 1) * w + c) as usize];
            }
            if c > 0 {
                marks[(r * w + c) as usize] += marks[(r * w + c - 1) as usize];
            }
            if r > 0 && c > 0 {
                marks[(r * w + c) as usize] -= marks[((r - 1) * w + c - 1) as usize];
            }
            if grid[r as usize][c as usize] == 0 && marks[(r * w + c) as usize] == 0 {
                return false;
            }
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2132i64;
    let mut grid: Vec<Vec<i64>> = Vec::new();
    for r in 0..400 {
        let mut row = Vec::new();
        for c in 0..500 {
            row.push(if r % 4 == 3 || c % 4 == 3 { 1 } else { 0 });
        }
        grid.push(row);
    }
    let mut stamped = 0i64;
    let mut check = 0i64;
    for round in 0..100i64 {
        let at = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 200000;
        let (r, c) = ((at / 500) as usize, (at % 500) as usize);
        grid[r][c] = 1 - grid[r][c];
        let h = next_random(&mut seed) % 3 + 1;
        let w = next_random(&mut seed) % 3 + 1;
        let fits = if possible_to_stamp(&grid, h, w) { 1 } else { 0 };
        grid[r][c] = 1 - grid[r][c];
        stamped += fits;
        check = (check * 31 + fits + at + round) % 1000000007;
    }
    println!("100 solves: {} stamped, checksum {}", stamped, check);
}
