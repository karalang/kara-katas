// LeetCode #1349 bench -- Rust: each row's students as a bit mask,
// best[mask] the most students so far with the last row seated as mask.

fn max_students(seats: &[Vec<char>]) -> i32 {
    let n = seats[0].len();
    let full = 1usize << n;
    let mut best = vec![-1i32; full];
    best[0] = 0;
    for row in seats {
        let mut good = 0usize;
        for j in 0..n {
            if row[j] == '.' {
                good |= 1 << j;
            }
        }
        let mut next = vec![-1i32; full];
        for mask in 0..full {
            if mask & good != mask || mask & (mask << 1) != 0 {
                continue;
            }
            let here = mask.count_ones() as i32;
            for prev in 0..full {
                if best[prev] < 0 || mask & (prev << 1) != 0 || mask & (prev >> 1) != 0 {
                    continue;
                }
                next[mask] = next[mask].max(best[prev] + here);
            }
        }
        best = next;
    }
    *best.iter().max().unwrap()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1349;
    let mut rooms: Vec<Vec<Vec<char>>> = Vec::new();
    for _ in 0..20 {
        let mut seats = Vec::new();
        for _ in 0..8 {
            let r: Vec<char> = (0..8).map(|_| if next_random(&mut seed) % 4 == 0 { '#' } else { '.' }).collect();
            seats.push(r);
        }
        rooms.push(seats);
    }
    let mut check: i64 = 0;
    for r in 0..3000i64 {
        let k = (check % 20) as usize;
        let i = ((check / 20) % 8) as usize;
        let j = ((check / 160) % 8) as usize;
        rooms[k][i][j] = if rooms[k][i][j] == '.' { '#' } else { '.' };
        check = (check * 31 + max_students(&rooms[k]) as i64 + r) % 1000000007;
    }
    println!("3000 rounds over 20 rooms of 8 by 8: checksum {}", check);
}
