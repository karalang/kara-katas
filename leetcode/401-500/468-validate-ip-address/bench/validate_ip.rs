// Benchmark for #468: mirror of validate_ip.kara (the ★ arm: split on the
// separator) on the same workload. The answer is a fresh String, as in
// the Kāra arm.

fn ipv4_part(part: &str) -> bool {
    if part.is_empty() || part.len() > 3 {
        return false;
    }
    let mut value = 0;
    for c in part.chars() {
        if !c.is_ascii_digit() {
            return false;
        }
        value = value * 10 + (c as i64 - 48);
    }
    if part.len() > 1 && part.starts_with('0') {
        return false;
    }
    value <= 255
}

fn ipv6_group(group: &str) -> bool {
    if group.is_empty() || group.len() > 4 {
        return false;
    }
    for c in group.chars() {
        if !c.is_ascii_hexdigit() {
            return false;
        }
    }
    true
}

fn valid_ip_address(query_ip: &str) -> String {
    if query_ip.contains('.') {
        let mut parts = 0;
        for part in query_ip.split('.') {
            if !ipv4_part(part) {
                return String::from("Neither");
            }
            parts += 1;
        }
        if parts == 4 {
            return String::from("IPv4");
        }
    } else if query_ip.contains(':') {
        let mut groups = 0;
        for group in query_ip.split(':') {
            if !ipv6_group(group) {
                return String::from("Neither");
            }
            groups += 1;
        }
        if groups == 8 {
            return String::from("IPv6");
        }
    }
    String::from("Neither")
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn pick(alphabet: &str, seed: &mut i64) -> char {
    let letters: Vec<char> = alphabet.chars().collect();
    letters[(next_random(seed) % letters.len() as i64) as usize]
}

fn random_query(seed: &mut i64) -> String {
    let kind = next_random(seed) % 5;
    let fault = next_random(seed) % 8;
    let mut s = String::new();
    if kind < 2 {
        let parts = if fault == 4 { [3, 5][(next_random(seed) % 2) as usize] } else { 4 };
        let at = next_random(seed) % parts;
        for p in 0..parts {
            if p > 0 {
                s.push('.');
            }
            let mut value = next_random(seed) % 256;
            if p == at && fault == 5 {
                s.push('0');
            }
            if p == at && fault == 6 {
                value = 256 + next_random(seed) % 744;
            }
            if p == at && fault == 7 {
                if next_random(seed) % 2 == 0 {
                    s.push(pick("aeFx", seed));
                }
                continue;
            }
            s.push_str(&format!("{value}"));
        }
    } else if kind < 4 {
        let groups = if fault == 4 { [7, 9][(next_random(seed) % 2) as usize] } else { 8 };
        let at = next_random(seed) % groups;
        for g in 0..groups {
            if g > 0 {
                s.push(':');
            }
            if g == at && fault == 6 {
                continue;
            }
            let length = if g == at && fault == 5 { 5 } else { 1 + next_random(seed) % 4 };
            let bad = if g == at && fault == 7 { next_random(seed) % length } else { -1 };
            for i in 0..length {
                if i == bad {
                    s.push(pick("gGxz", seed));
                } else {
                    s.push(pick("0123456789abcdefABCDEF", seed));
                }
            }
        }
    } else {
        let length = 1 + next_random(seed) % 15;
        for _ in 0..length {
            s.push(pick("0123456789aF.:g", seed));
        }
    }
    s
}

fn main() {
    let count = 100000;
    let rounds = 20;
    let mut seed: i64 = 468;
    let mut queries: Vec<String> = Vec::new();
    for _ in 0..count {
        queries.push(random_query(&mut seed));
    }
    let mut ipv4 = 0;
    let mut ipv6 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        for i in 0..count {
            let answer = valid_ip_address(&queries[i]);
            let code = if answer == "IPv4" {
                ipv4 += 1;
                1
            } else if answer == "IPv6" {
                ipv6 += 1;
                2
            } else {
                3
            };
            checksum = (checksum * 7 + code + i as i64) % 1000000007;
        }
    }
    println!("{rounds} rounds of {count} queries: {ipv4} IPv4, {ipv6} IPv6, checksum {checksum}");
}
