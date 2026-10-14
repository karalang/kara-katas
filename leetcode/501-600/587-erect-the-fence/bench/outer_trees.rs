// Benchmark for #587: Rust mirror of the ★ arm (the monotone chain); see
// outer_trees.kara. Each call copies the trees into a fresh `Vec`, sorts
// it with the standard library's stable sort, and removes repeats with
// `dedup`, as the Kāra arm does.

fn cross(o: (i64, i64), a: (i64, i64), b: (i64, i64)) -> i64 {
    (a.0 - o.0) * (b.1 - o.1) - (a.1 - o.1) * (b.0 - o.0)
}

fn outer_trees(trees: &[(i64, i64)]) -> Vec<(i64, i64)> {
    let mut points = trees.to_vec();
    points.sort();
    let mut fence: Vec<(i64, i64)> = Vec::new();
    for p in points.iter() {
        while fence.len() >= 2 && cross(fence[fence.len() - 2], fence[fence.len() - 1], *p) < 0 {
            fence.pop();
        }
        fence.push(*p);
    }
    let lower = fence.len();
    for p in points.iter().rev() {
        while fence.len() > lower && cross(fence[fence.len() - 2], fence[fence.len() - 1], *p) < 0 {
            fence.pop();
        }
        fence.push(*p);
    }
    fence.sort();
    fence.dedup();
    fence
}

// ---- benchmark --------------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count: i64 = 50;
    let rounds: i64 = 300;
    let mut seed: i64 = 587;
    let mut gardens: Vec<Vec<(i64, i64)>> = Vec::new();
    for _ in 0..count {
        let size = (1000 + next_random(&mut seed) % 2001) as usize;
        let mut taken = vec![false; 101 * 101];
        let mut trees: Vec<(i64, i64)> = Vec::new();
        while trees.len() < size {
            let x = next_random(&mut seed) % 101;
            let y = next_random(&mut seed) % 101;
            if !taken[(x * 101 + y) as usize] {
                taken[(x * 101 + y) as usize] = true;
                trees.push((x, y));
            }
        }
        gardens.push(trees);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for g in 0..count {
            let p = ((round * 7 + g) % count) as usize;
            let fence = outer_trees(&gardens[p]);
            let mut sum = 0;
            for t in fence.iter() {
                sum += t.0 * 101 + t.1;
            }
            total += fence.len() as i64;
            checksum = (checksum * 31 + sum) % 1000000007;
        }
    }
    println!("{} gardens, {} rounds: {} on the fence, checksum {}", count, rounds, total, checksum);
}
