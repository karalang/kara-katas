// LeetCode #1591: Strange Printer II -- the bench in Rust, mirroring
// printer.kara: bounding rectangles, an order graph as a 61 by 61 matrix,
// and Kahn's algorithm.

fn is_printable(target_grid: &[Vec<i32>]) -> bool {
    let rows = target_grid.len() as i64;
    let cols = target_grid[0].len() as i64;
    let mut top = vec![rows; 61];
    let mut bottom = vec![-1i64; 61];
    let mut left = vec![cols; 61];
    let mut right = vec![-1i64; 61];
    for r in 0..rows {
        for c in 0..cols {
            let k = target_grid[r as usize][c as usize] as usize;
            top[k] = top[k].min(r);
            bottom[k] = bottom[k].max(r);
            left[k] = left[k].min(c);
            right[k] = right[k].max(c);
        }
    }
    let mut after = vec![vec![false; 61]; 61];
    let mut before = vec![0i64; 61];
    for k in 1..61 {
        for r in top[k]..bottom[k] + 1 {
            for c in left[k]..right[k] + 1 {
                let other = target_grid[r as usize][c as usize] as usize;
                if other != k && !after[k][other] {
                    after[k][other] = true;
                    before[other] += 1;
                }
            }
        }
    }
    let mut ready: Vec<usize> = (1..61).filter(|&k| before[k] == 0).collect();
    let mut taken = 0;
    while let Some(k) = ready.pop() {
        taken += 1;
        for other in 1..61 {
            if after[k][other] {
                before[other] -= 1;
                if before[other] == 0 {
                    ready.push(other);
                }
            }
        }
    }
    taken == 60
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1591;
    let mut grids: Vec<Vec<Vec<i32>>> = Vec::new();
    for g in 0..4000 {
        let mut order: Vec<i32> = (1..61).collect();
        for i in (1..60).rev() {
            let j = (next_random(&mut seed) % (i as i64 + 1)) as usize;
            order.swap(i, j);
        }
        let mut grid = vec![vec![order[0]; 60]; 60];
        for &k in &order[1..] {
            let r1 = next_random(&mut seed) % 60;
            let r2 = next_random(&mut seed) % 60;
            let c1 = next_random(&mut seed) % 60;
            let c2 = next_random(&mut seed) % 60;
            for r in r1.min(r2)..r1.max(r2) + 1 {
                for c in c1.min(c2)..c1.max(c2) + 1 {
                    grid[r as usize][c as usize] = k;
                }
            }
        }
        if g % 2 == 1 {
            let r = next_random(&mut seed) % 60;
            let c = next_random(&mut seed) % 60;
            grid[r as usize][c as usize] = (next_random(&mut seed) % 60 + 1) as i32;
        }
        grids.push(grid);
    }
    let mut check: i64 = 0;
    let mut yes = 0;
    for grid in &grids {
        let ok = is_printable(grid);
        if ok {
            yes += 1;
        }
        check = (check * 31 + ok as i64 + 1) % 1000000007;
    }
    println!("4000 grids of 60 by 60: {} printable, checksum {}", yes, check);
}
