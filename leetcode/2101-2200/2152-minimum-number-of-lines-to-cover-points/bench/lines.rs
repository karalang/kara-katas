// LeetCode #2152: Minimum Number of Lines to Cover Points -- the
// benchmark's Rust mirror of lines.kara.

fn minimum_lines(points: &[Vec<i64>]) -> i64 {
    let n = points.len();
    let full = (1usize << n) - 1;
    let mut fewest: Vec<i64> = vec![n as i64 + 1; 1 << n];
    fewest[0] = 0;
    for mask in 0..full {
        if fewest[mask] > n as i64 {
            continue;
        }
        let mut i = 0;
        while (mask >> i) & 1 == 1 {
            i += 1;
        }
        let alone = mask | (1 << i);
        fewest[alone] = fewest[alone].min(fewest[mask] + 1);
        for j in i + 1..n {
            let mut line = 0usize;
            for k in 0..n {
                let cross = (points[j][0] - points[i][0]) * (points[k][1] - points[i][1]) - (points[j][1] - points[i][1]) * (points[k][0] - points[i][0]);
                if cross == 0 {
                    line |= 1 << k;
                }
            }
            fewest[mask | line] = fewest[mask | line].min(fewest[mask] + 1);
        }
    }
    fewest[full]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn free_place(points: &[Vec<i64>], seed: &mut i64) -> Vec<i64> {
    loop {
        let x = next_random(seed) % 7 - 3;
        let y = next_random(seed) % 7 - 3;
        let p = vec![x, y];
        if !points.contains(&p) {
            return p;
        }
    }
}

fn main() {
    let mut seed = 2152;
    let mut sets: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..4 {
        let mut points: Vec<Vec<i64>> = Vec::new();
        while points.len() < 10 {
            let p = free_place(&points, &mut seed);
            points.push(p);
        }
        sets.push(points);
    }
    let mut total = 0;
    let mut check = 0;
    for round in 0..2500 {
        for s in 0..4 {
            let at = (next_random(&mut seed) % 10) as usize;
            sets[s][at] = free_place(&sets[s], &mut seed);
            let lines = minimum_lines(&sets[s]);
            total += lines;
            check = (check * 31 + lines + round) % 1000000007;
        }
    }
    println!("10000 solves: {} lines in all, checksum {}", total, check);
}
