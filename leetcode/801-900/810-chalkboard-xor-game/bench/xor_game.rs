// LeetCode 810 -- Chalkboard XOR Game: the bench, with the ★ arm's XOR and
// count.
fn xor_game(nums: &[i64]) -> bool {
    let mut x = 0;
    for i in 0..nums.len() {
        x ^= nums[i];
    }
    x == 0 || nums.len() % 2 == 0
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

// 64 boards of 999 numbers are made once. Each round writes a new number
// into one place of the next board and asks who wins it.
fn main() {
    let mut seed = 810;
    let mut boards: Vec<Vec<i64>> = Vec::new();
    for _ in 0..64 {
        let mut board: Vec<i64> = Vec::new();
        for _ in 0..999 {
            board.push(next_random(&mut seed));
        }
        boards.push(board);
    }
    let rounds: i64 = 10000000;
    let mut wins: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        let k = (r % 64) as usize;
        boards[k][(r / 64 % 999) as usize] = next_random(&mut seed);
        let win = if xor_game(&boards[k]) { 1 } else { 0 };
        wins += win;
        check = (check * 131 + win + r % 1000) % 1000000007;
    }
    println!("{} rounds of 999 numbers: {} won by Alice, checksum {}", rounds, wins, check);
}
