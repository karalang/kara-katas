// Benchmark: LeetCode #959 Regions Cut By Slashes -- the ★ arm, four
// triangles per cell, on grids of 30 by 30, LeetCode's largest. Mirrors
// regions_by_slashes.kara, .c, .py and go-seq/.

fn find(parent: &mut [usize], x: usize) -> usize {
    let mut r = x;
    while parent[r] != r {
        r = parent[r];
    }
    let mut c = x;
    while parent[c] != r {
        let next = parent[c];
        parent[c] = r;
        c = next;
    }
    r
}

fn union(parent: &mut [usize], sets: &mut i64, a: usize, b: usize) {
    let ra = find(parent, a);
    let rb = find(parent, b);
    if ra != rb {
        parent[ra] = rb;
        *sets -= 1;
    }
}

fn regions_by_slashes(grid: &[String]) -> i64 {
    let n = grid.len();
    let mut parent: Vec<usize> = (0..4 * n * n).collect();
    let mut sets = (4 * n * n) as i64;
    for r in 0..n {
        let row = grid[r].as_bytes();
        for c in 0..n {
            // triangles 0 top, 1 right, 2 bottom, 3 left
            let t = 4 * (r * n + c);
            let ch = row[c];
            if ch == b' ' {
                union(&mut parent, &mut sets, t, t + 1);
                union(&mut parent, &mut sets, t + 1, t + 2);
                union(&mut parent, &mut sets, t + 2, t + 3);
            } else if ch == b'/' {
                union(&mut parent, &mut sets, t, t + 3);
                union(&mut parent, &mut sets, t + 1, t + 2);
            } else {
                union(&mut parent, &mut sets, t, t + 1);
                union(&mut parent, &mut sets, t + 2, t + 3);
            }
            if c + 1 < n {
                union(&mut parent, &mut sets, t + 1, t + 4 + 3);
            }
            if r + 1 < n {
                union(&mut parent, &mut sets, t + 2, t + 4 * n);
            }
        }
    }
    sets
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_grid(n: usize, blank: i64, seed: &mut i64) -> Vec<String> {
    let mut grid = Vec::new();
    for _ in 0..n {
        let mut row = String::new();
        for _ in 0..n {
            if next_random(seed) % 10 < blank {
                row.push(' ');
            } else if next_random(seed) % 2 == 0 {
                row.push('/');
            } else {
                row.push('\\');
            }
        }
        grid.push(row);
    }
    grid
}

fn main() {
    let rounds = 300;
    let mut seed = 959;
    let grids: Vec<Vec<String>> = (0..100)
        .map(|i| random_grid(30, i % 10, &mut seed))
        .collect();
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..100 {
            let k = regions_by_slashes(&grids[(r + i) % 100]);
            total += k;
            check = (check * 31 + k + i as i64) % 1000000007;
        }
    }
    println!("{rounds} rounds over 100 grids of 30 by 30: {total} regions, checksum {check}");
}
