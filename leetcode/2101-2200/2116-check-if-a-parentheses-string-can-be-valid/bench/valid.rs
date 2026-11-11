// LeetCode #2116: Check if a Parentheses String Can Be Valid -- the
// benchmark, the same algorithm as valid.kara: two greedy passes over the
// bytes.

fn can_be_valid(s: &[u8], locked: &[u8]) -> bool {
    let n = s.len();
    if n % 2 == 1 {
        return false;
    }
    let mut open = 0i64;
    for i in 0..n {
        if s[i] == b'(' || locked[i] == b'0' {
            open += 1;
        } else {
            open -= 1;
            if open < 0 {
                return false;
            }
        }
    }
    let mut close = 0i64;
    for i in (0..n).rev() {
        if s[i] == b')' || locked[i] == b'0' {
            close += 1;
        } else {
            close -= 1;
            if close < 0 {
                return false;
            }
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2116i64;
    let mut strings: Vec<Vec<u8>> = Vec::new();
    let mut locks: Vec<Vec<u8>> = Vec::new();
    let n = 50000i64;
    for k in 0..64 {
        let flip = if next_random(&mut seed) % 2 == 0 { next_random(&mut seed) % n } else { -1 };
        let mut s = Vec::new();
        let mut locked = Vec::new();
        let mut open = 0i64;
        for i in 0..n {
            let mut up = if open == 0 {
                true
            } else if open == n - i {
                false
            } else {
                next_random(&mut seed) % 2 == 0
            };
            open += if up { 1 } else { -1 };
            if i == flip {
                up = !up;
            }
            s.push(if up { b'(' } else { b')' });
            let unlocked = next_random(&mut seed) % 4 == 0 && k % 2 == 0;
            locked.push(if unlocked { b'0' } else { b'1' });
        }
        strings.push(s);
        locks.push(locked);
    }
    let mut valid = 0i64;
    let mut check = 0i64;
    for round in 0..40i64 {
        for a in 0..64usize {
            strings[a].extend_from_slice(b"()");
            locks[a].extend_from_slice(b"11");
            let got = can_be_valid(&strings[a], &locks[a]);
            if got {
                valid += 1;
            }
            check = (check * 31 + if got { round + a as i64 } else { 1 }) % 1000000007;
        }
    }
    println!("2560 solves: {} can be valid, checksum {}", valid, check);
}
