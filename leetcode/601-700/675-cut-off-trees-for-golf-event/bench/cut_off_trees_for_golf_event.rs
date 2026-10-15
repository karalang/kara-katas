// Benchmark for #675: a breadth-first search for each walk, as the Kara
// ★ arm.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn steps(forest: &[Vec<i64>], sr: i64, sc: i64, tr: i64, tc: i64) -> i64 {
    if sr == tr && sc == tc {
        return 0;
    }
    let rows = forest.len() as i64;
    let cols = forest[0].len() as i64;
    let mut seen = vec![false; (rows * cols) as usize];
    let mut queue: Vec<i64> = Vec::new();
    queue.push(sr * cols + sc);
    seen[(sr * cols + sc) as usize] = true;
    let moves = [(-1i64, 0i64), (1, 0), (0, -1), (0, 1)];
    let mut head = 0;
    let mut dist = 0;
    while head < queue.len() {
        let end = queue.len();
        dist += 1;
        while head < end {
            let cell = queue[head];
            head += 1;
            let r = cell / cols;
            let c = cell % cols;
            for &(dr, dc) in moves.iter() {
                let nr = r + dr;
                let nc = c + dc;
                if nr >= 0
                    && nr < rows
                    && nc >= 0
                    && nc < cols
                    && forest[nr as usize][nc as usize] != 0
                    && !seen[(nr * cols + nc) as usize]
                {
                    if nr == tr && nc == tc {
                        return dist;
                    }
                    seen[(nr * cols + nc) as usize] = true;
                    queue.push(nr * cols + nc);
                }
            }
        }
    }
    -1
}

fn cut_off_tree(forest: &[Vec<i64>]) -> i64 {
    let mut trees: Vec<(i64, i64, i64)> = Vec::new();
    for r in 0..forest.len() {
        for c in 0..forest[0].len() {
            if forest[r][c] > 1 {
                trees.push((forest[r][c], r as i64, c as i64));
            }
        }
    }
    trees.sort_by(|a, b| a.0.cmp(&b.0));
    let mut total = 0;
    let mut r = 0;
    let mut c = 0;
    for &(_, tr, tc) in trees.iter() {
        let d = steps(forest, r, c, tr, tc);
        if d < 0 {
            return -1;
        }
        total += d;
        r = tr;
        c = tc;
    }
    total
}

fn random_forest(seed: &mut i64, rows: i64, cols: i64, walls: i64, trees: i64) -> Vec<Vec<i64>> {
    let mut forest: Vec<Vec<i64>> = Vec::new();
    let mut spots: Vec<i64> = Vec::new();
    for r in 0..rows {
        let mut row: Vec<i64> = Vec::new();
        for c in 0..cols {
            let k = next_random(seed) % 100;
            if (r > 0 || c > 0) && k < walls {
                row.push(0);
            } else {
                row.push(1);
                if k < walls + trees {
                    spots.push(r * cols + c);
                }
            }
        }
        forest.push(row);
    }
    let mut i = spots.len() as i64;
    while i > 1 {
        let j = next_random(seed) % i;
        i -= 1;
        spots.swap(i as usize, j as usize);
    }
    for k in 0..spots.len() {
        forest[(spots[k] / cols) as usize][(spots[k] % cols) as usize] = 2 + k as i64 * 7;
    }
    forest
}

fn main() {
    let forests = 40;
    let mut seed: i64 = 675;
    let mut sum: i64 = 0;
    let mut reached = 0;
    for _ in 0..forests {
        let forest = random_forest(&mut seed, 50, 50, 10, 30);
        let got = cut_off_tree(&forest);
        if got >= 0 {
            reached += 1;
        }
        sum = (sum * 31 + got + 1) % 1000000007;
    }
    println!("{} forests of 50x50, {} reachable: checksum {}", forests, reached, sum);
}
