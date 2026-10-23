// LeetCode #877 bench: Rust mirror of stone_game.kara (the ★ arm, the
// best margin of every run of piles) on the same 1,000 games.

fn stone_game(piles: &[i64]) -> bool {
    let n = piles.len();
    let mut margin: Vec<Vec<i64>> = Vec::new();
    for i in 0..n {
        let mut row = Vec::new();
        for j in 0..n {
            row.push(if i == j { piles[i] } else { 0 });
        }
        margin.push(row);
    }
    for length in 2..n + 1 {
        for i in 0..n - length + 1 {
            let j = i + length - 1;
            margin[i][j] = (piles[i] - margin[i + 1][j]).max(piles[j] - margin[i][j - 1]);
        }
    }
    margin[0][n - 1] > 0
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_piles(seed: &mut i64, limit: i64) -> Vec<i64> {
    let mut piles = Vec::new();
    let mut total = 0;
    for _ in 0..500 {
        let p = next_random(seed) % limit + 1;
        piles.push(p);
        total += p;
    }
    if total % 2 == 0 {
        piles[0] = if piles[0] == limit { piles[0] - 1 } else { piles[0] + 1 };
    }
    piles
}

fn main() {
    let mut seed: i64 = 877;
    let mut rows: Vec<Vec<i64>> = Vec::new();
    for k in 0..20 {
        rows.push(random_piles(&mut seed, if k % 2 == 0 { 500 } else { 3 }));
    }
    let mut wins = 0;
    let mut check: i64 = 0;
    for k in 0..1000 {
        let answer = stone_game(&rows[k % 20]);
        if answer {
            wins += 1;
        }
        check = (check * 3 + if answer { 1 } else { 2 }) % 1000000007;
    }
    println!("1000 games of 500 piles: Alice wins {}, checksum {}", wins, check);
}
