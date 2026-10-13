// Benchmark for #499: Rust mirror of the ★ arm (Dijkstra over the places
// the ball stops); see the_maze_iii.kara. The queue is a BinaryHeap of
// Reverse((distance, instructions, row, column)), so it pops the least
// pair first as Kāra's min-first PriorityQueue does.
use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn find_shortest_way(maze: &[Vec<i64>], ball: &[i64], hole: &[i64]) -> String {
    let rows = maze.len() as i64;
    let cols = maze[0].len() as i64;
    let moves = [(1, 0, "d"), (0, -1, "l"), (0, 1, "r"), (-1, 0, "u")];
    let mut done = vec![vec![false; cols as usize]; rows as usize];
    let mut queue: BinaryHeap<Reverse<(i64, String, i64, i64)>> = BinaryHeap::new();
    queue.push(Reverse((0, String::new(), ball[0], ball[1])));
    while let Some(Reverse((dist, path, row, col))) = queue.pop() {
        if done[row as usize][col as usize] {
            continue;
        }
        done[row as usize][col as usize] = true;
        if row == hole[0] && col == hole[1] {
            return path;
        }
        for &(dr, dc, name) in &moves {
            let mut r = row;
            let mut c = col;
            let mut steps = 0;
            while r + dr >= 0 && r + dr < rows && c + dc >= 0 && c + dc < cols && maze[(r + dr) as usize][(c + dc) as usize] == 0 {
                r += dr;
                c += dc;
                steps += 1;
                if r == hole[0] && c == hole[1] {
                    break;
                }
            }
            if steps > 0 && !done[r as usize][c as usize] {
                queue.push(Reverse((dist + steps, path.clone() + name, r, c)));
            }
        }
    }
    "impossible".to_string()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 1,000 mazes of 100 by 100 (the problem's most), a wall in each
    // cell with odds of 1 in 4, with a ball and a hole in two different
    // open cells, built once. Then each is solved once.
    let mazes = 1000;
    let mut seed: i64 = 499;
    let mut all: Vec<Vec<Vec<i64>>> = Vec::new();
    let mut balls: Vec<Vec<i64>> = Vec::new();
    let mut holes: Vec<Vec<i64>> = Vec::new();
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
        let a = next_random(&mut seed) % open.len() as i64;
        let mut b = next_random(&mut seed) % (open.len() as i64 - 1);
        if b >= a {
            b += 1;
        }
        balls.push(vec![open[a as usize].0, open[a as usize].1]);
        holes.push(vec![open[b as usize].0, open[b as usize].1]);
        all.push(maze);
    }
    let mut reached = 0;
    let mut letters = 0;
    let mut checksum: i64 = 0;
    for k in 0..mazes {
        let way = find_shortest_way(&all[k], &balls[k], &holes[k]);
        if way != "impossible" {
            reached += 1;
            letters += way.len();
        }
        for ch in way.chars() {
            checksum = (checksum * 31 + ch as i64) % 1000000007;
        }
    }
    println!("{mazes} mazes of 100 by 100: the hole reached in {reached}, {letters} instructions in all, checksum {checksum}");
}
