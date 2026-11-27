// LeetCode #1812: Determine Color of a Chessboard Square -- the bench in
// Rust: the ★ arm over 3 * 10^7 calls, each of the 64 square names built
// once and drawn from the checksum so far.

fn square_is_white(coordinates: &str) -> bool {
    let bytes = coordinates.as_bytes();
    let file = (bytes[0] - b'a') as i64;
    let rank = (bytes[1] - b'1') as i64;
    (file + rank) % 2 == 1
}

fn main() {
    let mut names: Vec<String> = Vec::new();
    for file in "abcdefgh".chars() {
        for rank in 1..9 {
            names.push(format!("{}{}", file, rank));
        }
    }
    let mut check: i64 = 0;
    for call in 0..30000000i64 {
        let name = &names[((check + call) % 64) as usize];
        check = (check * 3 + if square_is_white(name) { 1 } else { 2 }) % 1000000007;
    }
    println!("30000000 calls: checksum {}", check);
}
