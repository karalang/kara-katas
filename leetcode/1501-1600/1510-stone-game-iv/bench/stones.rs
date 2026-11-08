// LeetCode #1510: Stone Game IV -- the bench: 40 piles of 50000 to 100000
// stones, each answered by the ★ arm.

fn winner_square_game(n: i64) -> bool {
    let n = n as usize;
    let mut wins = vec![false; n + 1];
    for pile in 1..n + 1 {
        let mut k = 1;
        while k * k <= pile {
            if !wins[pile - k * k] {
                wins[pile] = true;
                break;
            }
            k += 1;
        }
    }
    wins[n]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1510;
    let mut wins = 0;
    let mut check: i64 = 0;
    for _ in 0..40 {
        let n = 50000 + (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 50001;
        let w = winner_square_game(n);
        if w {
            wins += 1;
        }
        check = (check * 31 + if w { n } else { 0 } + 1) % 1000000007;
    }
    println!("40 piles of 50000 to 100000 stones: Alice wins {}, checksum {}", wins, check);
}
