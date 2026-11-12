// LeetCode #1138: Alphabet Board Path -- the bench, the ★ arm's algorithm:
// coordinates, up and left first, down and right after.

fn alphabet_board_path(target: String) -> String {
    let mut path = String::new();
    let mut row: i64 = 0;
    let mut col: i64 = 0;
    for c in target.chars() {
        let k = c as i64 - 'a' as i64;
        let (r, k_col) = (k / 5, k % 5);
        path.push_str(&"U".repeat((row - r).max(0) as usize));
        path.push_str(&"L".repeat((col - k_col).max(0) as usize));
        path.push_str(&"D".repeat((r - row).max(0) as usize));
        path.push_str(&"R".repeat((k_col - col).max(0) as usize));
        path.push('!');
        row = r;
        col = k_col;
    }
    path
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let letters: Vec<char> = "abcdefghijklmnopqrstuvwxyz".chars().collect();
    let mut seed: i64 = 1138;
    let mut targets: Vec<Vec<char>> = Vec::new();
    for _ in 0..1000 {
        let t: Vec<char> = (0..100).map(|_| letters[(next_random(&mut seed) % 26) as usize]).collect();
        targets.push(t);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..100usize {
        for j in 0..1000usize {
            targets[j][(round * 37 + j) % 100] = letters[(next_random(&mut seed) % 26) as usize];
            let target: String = targets[j].iter().collect();
            let path = alphabet_board_path(target);
            let mid = path.as_bytes()[path.len() / 2] as i64;
            total += path.len() as i64;
            check = (check * 31 + path.len() as i64 * 128 + mid) % 1000000007;
        }
    }
    println!("100 rounds over 1000 targets of 100 letters: lengths total {}, checksum {}", total, check);
}
