// LeetCode #2218: Maximum Value of K Coins From Piles -- bench mirror of
// coins.kara: a knapsack over the piles, best[j] the most j coins are
// worth so far, each pile tried at every count of its top coins with j
// running down.

fn max_value_of_coins(piles: &[Vec<i64>], k: usize) -> i64 {
    let mut best: Vec<i64> = vec![0; k + 1];
    for pile in piles {
        let mut prefix: Vec<i64> = vec![0];
        for &coin in pile {
            prefix.push(prefix[prefix.len() - 1] + coin);
        }
        for j in (1..k + 1).rev() {
            for t in 1..pile.len().min(j) + 1 {
                best[j] = best[j].max(best[j - t] + prefix[t]);
            }
        }
    }
    best[k]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

// a draw of 30 bits, since one draw stops at 32767
fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2218;
    let mut chests: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..20 {
        // 100 piles of 10 coins worth up to 10^5
        let mut piles: Vec<Vec<i64>> = Vec::new();
        for _ in 0..100 {
            piles.push((0..10).map(|_| wide_random(&mut seed) % 100000 + 1).collect());
        }
        chests.push(piles);
    }
    let mut check: i64 = 0;
    for a in 0..20 {
        for r in 0..4 {
            // punch: one coin is drawn again before each answer
            chests[a][r * 31 % 100][r] = wide_random(&mut seed) % 100000 + 1;
            check = (check * 31 + max_value_of_coins(&chests[a], 600)) % 1000000007;
        }
    }
    println!("20 sets of 100 piles of 10, k = 600, 4 punches: checksum {check}");
}
