// LeetCode #2868: The Wording Game -- the bench, as wording.kara: 20
// deals of 10^5 words, each played 20 times by the table arm.

fn table(words: &[String]) -> Vec<i64> {
    let mut top = vec![-1i64; 26];
    for (i, w) in words.iter().enumerate() {
        top[(w.as_bytes()[0] - b'a') as usize] = i as i64;
    }
    top
}

fn can_alice_win(a: &[String], b: &[String]) -> bool {
    let mut last = a[0].clone();
    let tops = [table(a), table(b)];
    let hands = [a, b];
    let mut turn = 1;
    loop {
        let c = (last.as_bytes()[0] - b'a') as usize;
        let same = tops[turn][c];
        if same >= 0 && hands[turn][same as usize] > last {
            last = hands[turn][same as usize].clone();
        } else if c < 25 && tops[turn][c + 1] >= 0 {
            last = hands[turn][tops[turn][c + 1] as usize].clone();
        } else {
            return turn == 1;
        }
        turn = 1 - turn;
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn deal(seed: &mut i64, n: i64, letters: i64, longest: i64) -> (Vec<String>, Vec<String>) {
    let mut words: Vec<String> = Vec::new();
    for _ in 0..n {
        let len = next_random(seed) % longest + 1;
        let word: String = (0..len)
            .map(|_| (b'a' + (next_random(seed) % letters) as u8) as char)
            .collect();
        words.push(word);
    }
    words.sort();
    words.dedup();
    let (mut a, mut b) = (Vec::new(), Vec::new());
    let first = (next_random(seed) % words.len() as i64) as usize;
    for (i, w) in words.iter().enumerate() {
        if i == first || (next_random(seed) % 2 == 0 && i != (first + 1) % words.len()) {
            a.push(w.clone());
        } else {
            b.push(w.clone());
        }
    }
    (a, b)
}

fn main() {
    let (count, rounds, n) = (20, 20, 100000);
    let mut seed = 2868;
    let deals: Vec<(Vec<String>, Vec<String>)> = (0..count)
        .map(|c| deal(&mut seed, n, if c % 2 == 0 { 26 } else { 5 }, 8))
        .collect();
    let mut wins = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (a, b) in deals.iter() {
            let win = can_alice_win(a, b);
            if win {
                wins += 1;
            }
            check = (check * 2 + r + if win { 1 } else { 0 }) % 1000000007;
        }
    }
    println!("{count} deals of {n} words, {rounds} rounds: Alice wins {wins}, checksum {check}");
}
