// LeetCode #929: Unique Email Addresses -- bench: one walk per address and
// a set. Mirrors num_unique_emails.kara.
use std::collections::HashSet;

fn num_unique_emails(emails: &[String]) -> i64 {
    let mut seen: HashSet<String> = HashSet::new();
    for e in emails {
        let mut out: Vec<u8> = Vec::new();
        let mut domain = false;
        let mut tagged = false;
        for c in e.bytes() {
            if domain {
                out.push(c);
            } else if c == b'@' {
                domain = true;
                out.push(c);
            } else if c == b'+' {
                tagged = true;
            } else if c != b'.' && !tagged {
                out.push(c);
            }
        }
        seen.insert(String::from_utf8(out).unwrap());
    }
    seen.len() as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let (rounds, count) = (300, 100);
    let mut seed = 929;
    let domains = [
        "@leetcode.com",
        "@lee.tcode.com",
        "@example.com",
        "@mail.example.com",
        "@a+b.com",
        "@ab.com",
        "@kara.dev.com",
        "@x.com",
    ];
    // count lists of 100 addresses, built once: a local name of 2 to 7
    // letters from "ab" with a dot before about one in four, a tag after a
    // '+' on half of them, and one of eight domains
    let mut lists: Vec<Vec<String>> = Vec::new();
    for _ in 0..count {
        let mut emails: Vec<String> = Vec::new();
        for _ in 0..100 {
            let mut b: Vec<u8> = Vec::new();
            let letters = 2 + next_random(&mut seed) % 6;
            for _ in 0..letters {
                if next_random(&mut seed) % 4 == 0 {
                    b.push(b'.');
                }
                b.push(b'a' + (next_random(&mut seed) % 2) as u8);
            }
            if next_random(&mut seed) % 2 == 0 {
                b.push(b'+');
                for _ in 0..next_random(&mut seed) % 10 {
                    b.push(b'a' + (next_random(&mut seed) % 26) as u8);
                }
            }
            let mut e = String::from_utf8(b).unwrap();
            e.push_str(domains[(next_random(&mut seed) % 8) as usize]);
            emails.push(e);
        }
        lists.push(emails);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        // each round visits every list, starting from a different one
        for i in 0..count {
            let a = num_unique_emails(&lists[(r + i) % count]);
            total += a;
            check = (check * 1000003 + a) % 1000000007;
        }
    }
    println!("{rounds} rounds over {count} lists of 100 addresses: answers summing to {total}, checksum {check}");
}
