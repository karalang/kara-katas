// LeetCode #2120: Execution of All Suffix Instructions Staying in a Grid
// -- the benchmark, the same algorithm as suffix.kara: each suffix
// simulated, 40 grids built once, 20 rounds with every start one row
// lower than in the round before.

fn execute_instructions(n: i64, start_pos: &[i64], s: &[u8]) -> Vec<i64> {
    let m = s.len();
    let mut answer = Vec::new();
    for i in 0..m {
        let mut row = start_pos[0];
        let mut col = start_pos[1];
        let mut count = 0;
        for j in i..m {
            match s[j] {
                b'L' => col -= 1,
                b'R' => col += 1,
                b'U' => row -= 1,
                _ => row += 1,
            }
            if row < 0 || row >= n || col < 0 || col >= n {
                break;
            }
            count += 1;
        }
        answer.push(count);
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2120;
    let mut grids: Vec<(i64, i64, i64, Vec<u8>)> = Vec::new();
    for _ in 0..40 {
        let n = next_random(&mut seed) % 401 + 100;
        let row = next_random(&mut seed) % n;
        let col = next_random(&mut seed) % n;
        let mut s = Vec::new();
        for _ in 0..500 {
            s.push(b"LRUD"[(next_random(&mut seed) % 4) as usize]);
        }
        grids.push((n, row, col, s));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..20 {
        for (n, row, col, s) in grids.iter() {
            let start = vec![(row + round) % n, *col];
            for c in execute_instructions(*n, &start, s) {
                total += c;
                check = (check * 31 + c) % 1000000007;
            }
        }
    }
    println!("800 solves: {} moves, checksum {}", total, check);
}
