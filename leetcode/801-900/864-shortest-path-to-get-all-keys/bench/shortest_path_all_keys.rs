// LeetCode #864: Shortest Path to Get All Keys -- Rust mirror of the bench
// program (the ★ arm, breadth-first search over (cell, keys held) states).
use std::collections::VecDeque;

fn shortest_path_all_keys(grid: &[String]) -> i64 {
    let rows = grid.len() as i64;
    let cols = grid[0].len() as i64;
    let mut cells: Vec<u8> = Vec::new();
    for row in grid {
        cells.extend_from_slice(row.as_bytes());
    }
    let size = cells.len() as i64;
    let mut start = 0;
    let mut keys = 0;
    for i in 0..size {
        let b = cells[i as usize];
        if b == b'@' {
            start = i;
        } else if (b'a'..=b'f').contains(&b) {
            keys += 1;
        }
    }
    let all = (1i64 << keys) - 1;
    let mut seen = vec![false; (size << keys) as usize];
    let mut queue: VecDeque<(i64, i64, i64)> = VecDeque::new();
    seen[start as usize] = true;
    queue.push_back((start, 0, 0));
    while let Some((cell, held, steps)) = queue.pop_front() {
        if held == all {
            return steps;
        }
        let r = cell / cols;
        let c = cell % cols;
        for (dr, dc) in [(-1, 0), (1, 0), (0, -1), (0, 1)] {
            let nr = r + dr;
            let nc = c + dc;
            if nr < 0 || nr >= rows || nc < 0 || nc >= cols {
                continue;
            }
            let next = nr * cols + nc;
            let b = cells[next as usize];
            if b == b'#' {
                continue;
            }
            if (b'A'..=b'F').contains(&b) && held & (1 << (b - b'A')) == 0 {
                continue;
            }
            let mut now = held;
            if (b'a'..=b'f').contains(&b) {
                now = held | (1 << (b - b'a'));
            }
            let state = (now * size + next) as usize;
            if !seen[state] {
                seen[state] = true;
                queue.push_back((next, now, steps + 1));
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
    let (rows, cols, rounds) = (30i64, 30i64, 1000);
    let mut seed = 864;
    let mut cells: Vec<u8> = Vec::new();
    for _ in 0..rows * cols {
        cells.push(if next_random(&mut seed) % 100 < 20 { b'#' } else { b'.' });
    }
    for i in 0..12u8 {
        let mut at = next_random(&mut seed) % (rows * cols);
        while cells[at as usize] != b'.' {
            at = next_random(&mut seed) % (rows * cols);
        }
        cells[at as usize] = if i < 6 { b'a' + i } else { b'A' + i - 6 };
    }
    let (mut reached, mut total, mut check) = (0i64, 0i64, 0i64);
    for _ in 0..rounds {
        let mut start = next_random(&mut seed) % (rows * cols);
        while cells[start as usize] != b'.' {
            start = next_random(&mut seed) % (rows * cols);
        }
        cells[start as usize] = b'@';
        let mut grid: Vec<String> = Vec::new();
        for r in 0..rows {
            let mut row = String::new();
            for c in 0..cols {
                row.push(cells[(r * cols + c) as usize] as char);
            }
            grid.push(row);
        }
        cells[start as usize] = b'.';
        let moves = shortest_path_all_keys(&grid);
        if moves >= 0 {
            reached += 1;
            total += moves;
        }
        check = (check * 31 + moves + 2) % 1000000007;
    }
    println!("{rounds} starts on a 30 by 30 grid: {reached} reach every key, moves sum to {total}, checksum {check}");
}
