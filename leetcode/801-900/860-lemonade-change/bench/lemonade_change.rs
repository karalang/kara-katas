// LeetCode #860: Lemonade Change -- Rust mirror of the bench program (the ★
// arm, count the fives and tens, pay a twenty with a ten when there is one).

fn lemonade_change(bills: &[i64]) -> bool {
    let mut fives: i64 = 0;
    let mut tens: i64 = 0;
    for &b in bills {
        if b == 5 {
            fives += 1;
        } else if b == 10 {
            if fives == 0 {
                return false;
            }
            fives -= 1;
            tens += 1;
        } else if tens > 0 && fives > 0 {
            tens -= 1;
            fives -= 1;
        } else if fives >= 3 {
            fives -= 3;
        } else {
            return false;
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: i64 = 100000;
    let mut seed: i64 = 860;
    let mut bills: Vec<i64> = Vec::new();
    let mut fives: i64 = 0;
    let mut tens: i64 = 0;
    for _ in 0..n {
        let r = next_random(&mut seed) % 10;
        if r >= 8 && tens > 0 && fives > 0 {
            bills.push(20);
            tens -= 1;
            fives -= 1;
        } else if r >= 8 && fives >= 3 {
            bills.push(20);
            fives -= 3;
        } else if r >= 5 && fives > 0 {
            bills.push(10);
            fives -= 1;
            tens += 1;
        } else {
            bills.push(5);
            fives += 1;
        }
    }
    let mut served: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..1000i64 {
        let i = (next_random(&mut seed) % n) as usize;
        let old = bills[i];
        bills[i] = if old == 5 { 10 } else if old == 10 { 20 } else { 5 };
        let yes = lemonade_change(&bills);
        bills[i] = old;
        if yes {
            served += 1;
        }
        check = (check * 31 + if yes { r + 2 } else { 1 }) % 1000000007;
    }
    println!("1000 rounds on 100000 bills: {} served, checksum {}", served, check);
}
