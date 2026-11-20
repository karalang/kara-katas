// LeetCode #1706: Where Will the Ball Fall -- the bench's Rust mirror: the
// ★ arm on 1000 random boxes of 100 by 100, all drawn first, each answered
// 100 times.

// each ball followed down a row at a time
fn find_ball(grid: &[Vec<i32>]) -> Vec<i32> {
    let n = grid[0].len() as i64;
    let mut answer: Vec<i32> = Vec::new();
    for start in 0..n {
        let mut c = start;
        for row in grid.iter() {
            let next = c + row[c as usize] as i64;
            if next < 0 || next >= n || row[next as usize] != row[c as usize] {
                c = -1;
                break;
            }
            c = next;
        }
        answer.push(c as i32);
    }
    answer
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 1000;
    let rounds = 100;
    let side = 100;
    let mut seed = 1706;
    let mut boxes: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..count {
        // long runs of one slope: a board turns the other way one time in 20
        let mut grid: Vec<Vec<i32>> = Vec::new();
        for _ in 0..side {
            let mut row: Vec<i32> = Vec::new();
            let mut board: i32 = 1;
            for _ in 0..side {
                if next_random(&mut seed) % 20 == 0 {
                    board = -board;
                }
                row.push(board);
            }
            grid.push(row);
        }
        boxes.push(grid);
    }
    let mut out: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for grid in boxes.iter() {
            let answer = find_ball(grid);
            for &a in answer.iter() {
                if a >= 0 {
                    out += 1;
                }
                check = (check * 31 + a as i64 + 2 + r) % 1000000007;
            }
        }
    }
    println!("{count} boxes of {side} by {side}, {rounds} rounds: {out} balls out, checksum {check}");
}
