// LeetCode #1222 bench, Rust mirror of the Kāra ★ arm: mark the queens on
// an 8 by 8 board, then walk out from the king in each of the eight
// directions, over 5000 random boards of 1 to 63 queens drawn once, 50
// passes; checksum of the attackers in the order found.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn queens_attackthe_king(queens: &[Vec<i64>], king: &[i64]) -> Vec<Vec<i64>> {
    let mut board = [[false; 8]; 8];
    for q in queens {
        board[q[0] as usize][q[1] as usize] = true;
    }
    let mut attackers: Vec<Vec<i64>> = Vec::new();
    for dx in -1i64..=1 {
        for dy in -1i64..=1 {
            if dx == 0 && dy == 0 {
                continue;
            }
            let mut x = king[0] + dx;
            let mut y = king[1] + dy;
            while x >= 0 && x < 8 && y >= 0 && y < 8 {
                if board[x as usize][y as usize] {
                    attackers.push(vec![x, y]);
                    break;
                }
                x += dx;
                y += dy;
            }
        }
    }
    attackers
}

fn main() {
    let mut seed: i64 = 1222;
    let mut boards: Vec<(Vec<Vec<i64>>, Vec<i64>)> = Vec::new();
    for _ in 0..5000 {
        let count = next_random(&mut seed) % 63 + 1;
        let mut squares: Vec<i64> = (0..64).collect();
        for k in 0..(count + 1) as usize {
            let j = k + (next_random(&mut seed) % (64 - k as i64)) as usize;
            squares.swap(k, j);
        }
        let queens: Vec<Vec<i64>> = squares[0..count as usize].iter().map(|s| vec![s / 8, s % 8]).collect();
        let king = vec![squares[count as usize] / 8, squares[count as usize] % 8];
        boards.push((queens, king));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..200 {
        for (queens, king) in boards.iter() {
            let attackers = queens_attackthe_king(queens, king);
            total += attackers.len() as i64;
            for a in attackers.iter() {
                check = (check * 131 + a[0] * 8 + a[1] + 1) % 1000000007;
            }
        }
    }
    println!("5000 boards of 1 to 63 queens, 200 passes: attackers total {}, checksum {}", total, check);
}
