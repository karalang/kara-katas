// LeetCode #2312: Selling Pieces of Wood -- the bench, the ★ arm in
// Rust. Bottom up over every size: each piece its own price or the most
// of any one cut across it.

fn selling_wood(m: usize, n: usize, prices: &[(usize, usize, i64)]) -> i64 {
    let mut best = vec![vec![0i64; n + 1]; m + 1];
    for &(h, w, price) in prices {
        best[h][w] = price;
    }
    for h in 1..=m {
        for w in 1..=n {
            for i in 1..h {
                best[h][w] = best[h][w].max(best[i][w] + best[h - i][w]);
            }
            for j in 1..w {
                best[h][w] = best[h][w].max(best[h][j] + best[h][w - j]);
            }
        }
    }
    best[m][n]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2312i64;
    let mut lists: Vec<Vec<(usize, usize, i64)>> = Vec::new();
    for _ in 0..10 {
        let mut used = vec![false; 200 * 200];
        let mut prices = Vec::new();
        for _ in 0..2000 {
            let h = (next_random(&mut seed) % 200 + 1) as usize;
            let w = (next_random(&mut seed) % 200 + 1) as usize;
            let price = next_random(&mut seed) % 1000000 + 1;
            if !used[(h - 1) * 200 + w - 1] {
                used[(h - 1) * 200 + w - 1] = true;
                prices.push((h, w, price));
            }
        }
        lists.push(prices);
    }
    let mut check = 0i64;
    for p in 0..2i64 {
        for a in 0..10 {
            let prices: Vec<(usize, usize, i64)> = lists[a].iter().map(|&(h, w, price)| (h, w, price + p)).collect();
            check = (check * 31 + selling_wood(200, 200, &prices)) % 1000000007;
        }
    }
    println!("2 passes over 10 lists of 2000 prices on 200 by 200: checksum {}", check);
}
