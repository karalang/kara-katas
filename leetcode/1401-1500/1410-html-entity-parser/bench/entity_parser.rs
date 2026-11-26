// LeetCode #1410 bench, Rust: the same walk, at each `&` the name up to the
// next `;` within seven characters looked up, workload and checksum as
// entity_parser.kara.

fn entity_parser(text: &str) -> String {
    let mut out = String::new();
    let mut i = 0;
    while i < text.len() {
        if text[i..].starts_with('&') {
            let window = &text[i..(i + 7).min(text.len())];
            if let Some(end) = window.find(';') {
                let symbol = match &window[..end + 1] {
                    "&quot;" => "\"",
                    "&apos;" => "'",
                    "&amp;" => "&",
                    "&gt;" => ">",
                    "&lt;" => "<",
                    "&frasl;" => "/",
                    _ => "",
                };
                if !symbol.is_empty() {
                    out.push_str(symbol);
                    i += end + 1;
                    continue;
                }
            }
        }
        out.push_str(&text[i..i + 1]);
        i += 1;
    }
    out
}

fn main() {
    let pieces = [
        "a", "b", " ", "&", ";", "&quot;", "&apos;", "&amp;", "&gt;", "&lt;", "&frasl;", "&amp", "&gt", "&quot",
        "&ambassador;", "&lt;;", "&&", "amp;", "&frasl",
    ];
    let mut seed: i64 = 1410;
    let mut pool = String::new();
    while pool.len() < 300000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        pool.push_str(pieces[(seed / 65536 % pieces.len() as i64) as usize]);
    }
    let mut check: i64 = 0;
    for _ in 0..300 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let start = (seed / 65536 % (pool.len() as i64 - 100000)) as usize;
        let out = entity_parser(&pool[start..start + 100000]);
        let mut sum: i64 = 0;
        for &b in out.as_bytes() {
            sum += b as i64;
        }
        check = (check * 131 + out.len() as i64 + sum) % 1000000007;
    }
    println!("300 windows of 10^5 characters: checksum {}", check);
}
