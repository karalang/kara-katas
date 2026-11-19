// LeetCode #2337: Move Pieces to Obtain a String -- the bench, the ★ arm
// in Rust: two indices walking the start's and the target's bytes
// together, each skipping blanks, the pieces matched in order and each
// `L` no later in the target, each `R` no earlier.

fn can_change(start: &str, target: &str) -> bool {
    let a = start.as_bytes();
    let b = target.as_bytes();
    let n = a.len();
    let (mut i, mut j) = (0usize, 0usize);
    loop {
        while i < n && a[i] == b'_' {
            i += 1;
        }
        while j < n && b[j] == b'_' {
            j += 1;
        }
        if i == n || j == n {
            return i == n && j == n;
        }
        if a[i] != b[j] {
            return false;
        }
        if a[i] == b'L' && i < j {
            return false;
        }
        if a[i] == b'R' && i > j {
            return false;
        }
        i += 1;
        j += 1;
    }
}

fn scrambled(index: i64) -> i64 {
    index * 2654435761 % 2147483647
}

fn main() {
    let mut pairs: Vec<(String, String)> = Vec::new();
    for q in 0..10i64 {
        let mut cells: Vec<u8> = (0..100000i64)
            .map(|i| match scrambled(q * 100000 + i) % 4 {
                0 => b'L',
                1 => b'R',
                _ => b'_',
            })
            .collect();
        let start = String::from_utf8(cells.clone()).unwrap();
        for _ in 0..3 {
            for i in 1..100000 {
                if cells[i] == b'L' && cells[i - 1] == b'_' {
                    cells[i - 1] = b'L';
                    cells[i] = b'_';
                }
            }
            for i in (0..99999).rev() {
                if cells[i] == b'R' && cells[i + 1] == b'_' {
                    cells[i + 1] = b'R';
                    cells[i] = b'_';
                }
            }
        }
        if q % 2 == 1 {
            let first = cells.iter().position(|&c| c != b'_').unwrap();
            cells[first] = if cells[first] == b'L' { b'R' } else { b'L' };
        }
        pairs.push((start, String::from_utf8(cells).unwrap()));
    }
    let mut check = 0i64;
    for p in 0..10i64 {
        for (start, target) in &pairs {
            let can = can_change(start, target);
            check = (check * 31 + if can { 2 } else { 1 } + p) % 1000000007;
        }
    }
    println!("10 passes over 10 pairs of 10^5 places: checksum {}", check);
}
