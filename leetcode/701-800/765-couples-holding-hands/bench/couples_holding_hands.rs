// LeetCode 765 — Couples Holding Hands: benchmark, the ★ arm in Rust.
// 1,000,000 random rows of 60 seats.

fn min_swaps_couples(mut row: Vec<i64>) -> i64 {
    let mut seat_of = vec![0usize; row.len()];
    for (i, &person) in row.iter().enumerate() {
        seat_of[person as usize] = i;
    }
    let mut swaps = 0;
    let mut i = 0;
    while i < row.len() {
        let partner = row[i] ^ 1;
        if row[i + 1] != partner {
            let j = seat_of[partner as usize];
            let moved = row[i + 1];
            row[j] = moved;
            seat_of[moved as usize] = j;
            row[i + 1] = partner;
            seat_of[partner as usize] = i + 1;
            swaps += 1;
        }
        i += 2;
    }
    swaps
}

fn main() {
    let mut seed: i64 = 765;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let rounds = 1000000;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        let mut row: Vec<i64> = (0..60).collect();
        for i in 0..60 {
            let j = i + (next_random() % (60 - i as i64)) as usize;
            row.swap(i, j);
        }
        let swaps = min_swaps_couples(row);
        total += swaps;
        check = (check * 31 + swaps) % 1000000007;
    }
    println!("{} rows of 60 seats: {} swaps in all, checksum {}", rounds, total, check);
}
