// LeetCode #2347: Best Poker Hand -- the bench, the ★ arm in Rust: a flush
// when every suit equals the first; otherwise the most cards of one rank,
// counted in a table of 14, names the hand.

fn best_hand(ranks: &[i64], suits: &[char]) -> String {
    let mut flush = true;
    for &s in suits {
        if s != suits[0] {
            flush = false;
        }
    }
    if flush {
        return "Flush".to_string();
    }
    let mut count = vec![0i64; 14];
    let mut most = 0;
    for &r in ranks {
        count[r as usize] += 1;
        most = most.max(count[r as usize]);
    }
    if most >= 3 {
        "Three of a Kind".to_string()
    } else if most == 2 {
        "Pair".to_string()
    } else {
        "High Card".to_string()
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // five different cards of 52, any card already in the hand drawn
    // again
    let mut seed = 2347i64;
    let mut hands: Vec<(Vec<i64>, Vec<char>)> = Vec::new();
    for _ in 0..100000 {
        let mut cards: Vec<i64> = Vec::new();
        while cards.len() < 5 {
            let card = next_random(&mut seed) % 52;
            if !cards.contains(&card) {
                cards.push(card);
            }
        }
        let ranks: Vec<i64> = cards.iter().map(|c| c % 13 + 1).collect();
        let suits: Vec<char> = cards.iter().map(|c| (97 + c / 13) as u8 as char).collect();
        hands.push((ranks, suits));
    }
    let mut check = 0i64;
    for p in 0..30i64 {
        for (ranks, suits) in &hands {
            check = (check * 31 + best_hand(ranks, suits).len() as i64 + p) % 1000000007;
        }
    }
    println!("30 passes over 10^5 hands: checksum {}", check);
}
