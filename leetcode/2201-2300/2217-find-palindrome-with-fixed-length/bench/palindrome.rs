// LeetCode #2217: Find Palindrome With Fixed Length -- bench mirror of
// palindrome.kara: the q-th half is 10^(half - 1) + q - 1, mirrored by
// arithmetic, the middle digit of an odd length used once.

fn kth_palindrome(queries: &[i64], int_length: i64) -> Vec<i64> {
    let half = (int_length + 1) / 2;
    let mut low: i64 = 1;
    for _ in 1..half {
        low *= 10;
    }
    let mut answer: Vec<i64> = Vec::new();
    for &q in queries {
        let first = low + q - 1;
        if first >= low * 10 {
            answer.push(-1);
            continue;
        }
        let mut palindrome = first;
        let mut rest = if int_length % 2 == 1 { first / 10 } else { first };
        while rest > 0 {
            palindrome = palindrome * 10 + rest % 10;
            rest /= 10;
        }
        answer.push(palindrome);
    }
    answer
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

// queries up to twice the count of palindromes of the length, so about
// half of them have none
fn query(seed: &mut i64, length: i64) -> i64 {
    let mut count: i64 = 9;
    for _ in 0..(length - 1) / 2 {
        count *= 10;
    }
    wide_random(seed) % (2 * count) + 1
}

fn main() {
    let mut seed = 2217;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for a in 0..30 {
        // 5 * 10^4 queries for each length from 1 to 15 in turn
        let length = a % 15 + 1;
        lists.push((0..50000).map(|_| query(&mut seed, length)).collect());
    }
    let mut check: i64 = 0;
    for a in 0..30 {
        let length = a as i64 % 15 + 1;
        for r in 0..10 {
            // punch: one query is drawn again before each answer
            lists[a][r * 4999] = query(&mut seed, length);
            for p in kth_palindrome(&lists[a], length) {
                check = (check * 31 + p + 1) % 1000000007;
            }
        }
    }
    println!("30 lists of 5 * 10^4 queries, 10 punches: checksum {check}");
}
