// Benchmark for #505 in Rust: the ★ arm (Dijkstra over the cells the
// ball can stop in); see ../shortest_distance.kara. A BinaryHeap of
// Reverse((distance, row, column)) is the smallest-first queue.
use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn shortest_distance(maze: &[Vec<i64>], start: &[i64], destination: &[i64]) -> i64 {
    let rows = maze.len() as i64;
    let cols = maze[0].len() as i64;
    let mut best = vec![vec![-1i64; cols as usize]; rows as usize];
    let mut queue = BinaryHeap::new();
    queue.push(Reverse((0i64, start[0], start[1])));
    let moves = [(-1i64, 0i64), (1, 0), (0, -1), (0, 1)];
    while let Some(Reverse((d, r, c))) = queue.pop() {
        if best[r as usize][c as usize] != -1 {
            continue;
        }
        best[r as usize][c as usize] = d;
        if r == destination[0] && c == destination[1] {
            return d;
        }
        for (dr, dc) in moves {
            let mut nr = r;
            let mut nc = c;
            let mut steps = 0;
            while nr + dr >= 0
                && nr + dr < rows
                && nc + dc >= 0
                && nc + dc < cols
                && maze[(nr + dr) as usize][(nc + dc) as usize] == 0
            {
                nr += dr;
                nc += dc;
                steps += 1;
            }
            if steps > 0 && best[nr as usize][nc as usize] == -1 {
                queue.push(Reverse((d + steps, nr, nc)));
            }
        }
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 2,000 mazes of 100 by 100 (the problem's most), a wall in each
    // cell with odds of 1 in 4, with a start and a destination in two
    // different open cells, built once. Then each is solved once.
    let mazes = 2000;
    let mut seed: i64 = 505;
    let mut all: Vec<Vec<Vec<i64>>> = Vec::new();
    let mut starts: Vec<Vec<i64>> = Vec::new();
    let mut destinations: Vec<Vec<i64>> = Vec::new();
    for _ in 0..mazes {
        let mut maze: Vec<Vec<i64>> = Vec::new();
        let mut open: Vec<(i64, i64)> = Vec::new();
        for r in 0..100 {
            let mut line: Vec<i64> = Vec::new();
            for c in 0..100 {
                if next_random(&mut seed) % 4 == 0 {
                    line.push(1);
                } else {
                    line.push(0);
                    open.push((r, c));
                }
            }
            maze.push(line);
        }
        let n = open.len() as i64;
        let a = next_random(&mut seed) % n;
        let mut b = next_random(&mut seed) % (n - 1);
        if b >= a {
            b += 1;
        }
        starts.push(vec![open[a as usize].0, open[a as usize].1]);
        destinations.push(vec![open[b as usize].0, open[b as usize].1]);
        all.push(maze);
    }
    let mut reached = 0;
    let mut total = 0;
    let mut checksum: i64 = 0;
    for k in 0..mazes {
        let d = shortest_distance(&all[k], &starts[k], &destinations[k]);
        if d != -1 {
            reached += 1;
            total += d;
        }
        checksum = (checksum * 31 + d + 1) % 1000000007;
    }
    println!("{mazes} mazes of 100 by 100: the destination reached in {reached}, distance {total} in all, checksum {checksum}");
}
