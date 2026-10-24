// LeetCode #937: Reorder Data in Log Files -- bench: two lists and a
// sort. Mirrors reorder_log_files.kara, .c, .py and go-seq/.

struct LogEntry {
    contents: String,
    id: String,
    log: String,
}

fn reorder_log_files(logs: &[String]) -> Vec<String> {
    let mut letters: Vec<LogEntry> = Vec::new();
    let mut digits: Vec<String> = Vec::new();
    for log in logs {
        let cut = log.find(' ').unwrap();
        let contents = log[cut + 1..].to_string();
        let first = contents.as_bytes()[0];
        if first.is_ascii_digit() {
            digits.push(log.clone());
        } else {
            letters.push(LogEntry {
                contents,
                id: log[..cut].to_string(),
                log: log.clone(),
            });
        }
    }
    letters.sort_by(|a, b| {
        if a.contents != b.contents {
            a.contents.cmp(&b.contents)
        } else {
            a.id.cmp(&b.id)
        }
    });
    let mut out: Vec<String> = Vec::new();
    for e in &letters {
        out.push(e.log.clone());
    }
    for d in &digits {
        out.push(d.clone());
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds: i64 = 200;
    let count: i64 = 200;
    let mut seed: i64 = 937;
    let mut lists: Vec<Vec<String>> = Vec::new();
    for _ in 0..count {
        let mut logs: Vec<String> = Vec::new();
        for i in 0..100 {
            let mut log = String::new();
            log.push((97 + next_random(&mut seed) % 26) as u8 as char);
            log.push_str(&i.to_string());
            let digits = next_random(&mut seed) % 2 == 1;
            let size = (20 + next_random(&mut seed) % 81) as usize;
            while log.len() + 2 <= size {
                let mut w = (1 + next_random(&mut seed) % 8) as usize;
                if log.len() + 1 + w > size {
                    w = size - log.len() - 1;
                }
                log.push(' ');
                for _ in 0..w {
                    if digits {
                        log.push((48 + next_random(&mut seed) % 10) as u8 as char);
                    } else {
                        log.push((97 + next_random(&mut seed) % 5) as u8 as char);
                    }
                }
            }
            logs.push(log);
        }
        lists.push(logs);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..count {
            let out = reorder_log_files(&lists[((r + i) % count) as usize]);
            total += out.len() as i64;
            for log in &out {
                for &b in log.as_bytes() {
                    if b == b' ' {
                        break;
                    }
                    check = (check * 131 + b as i64) % 1000000007;
                }
            }
        }
    }
    println!("{rounds} rounds over {count} lists of 100 logs: {total} logs, checksum {check}");
}
