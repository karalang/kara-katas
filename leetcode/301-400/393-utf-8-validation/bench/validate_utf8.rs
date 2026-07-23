fn lead_len(b: u8) -> i64 {
    if b & 0x80 == 0x00 {
        1
    } else if b & 0xE0 == 0xC0 {
        2
    } else if b & 0xF0 == 0xE0 {
        3
    } else if b & 0xF8 == 0xF0 {
        4
    } else {
        0
    }
}

fn is_continuation(b: u8) -> bool {
    b & 0xC0 == 0x80
}

fn validate_window(data: &[u8], base: i64, w: i64) -> bool {
    let end = base + w;
    let mut i = base;
    while i < end {
        let need = lead_len(data[i as usize]);
        if need == 0 {
            return false;
        }
        if i + need > end {
            return false;
        }
        let mut k = 1i64;
        while k < need {
            if !is_continuation(data[(i + k) as usize]) {
                return false;
            }
            k += 1;
        }
        i += need;
    }
    true
}

fn main() {
    let records: i64 = 40000;
    let w: i64 = 32;
    let passes: i64 = 60;
    let total = records * w;

    let mut data = vec![0u8; total as usize];

    let mut state: i64 = 12345;
    for rec in 0..records {
        let base = rec * w;
        let mut filled = 0i64;
        while filled < w {
            state = (state * 1103515245 + 12345) & 2147483647;
            let r = state >> 16;
            let cat = r % 100;
            let sub = r / 100;
            let rem = w - filled;
            if cat < 8 {
                data[(base + filled) as usize] = (128 + (sub % 64)) as u8;
                filled += 1;
            } else if cat < 60 || rem < 2 {
                data[(base + filled) as usize] = (sub % 128) as u8;
                filled += 1;
            } else if cat < 80 || rem < 3 {
                data[(base + filled) as usize] = (192 + (sub % 32)) as u8;
                data[(base + filled + 1) as usize] = (128 + (sub % 64)) as u8;
                filled += 2;
            } else if cat < 93 || rem < 4 {
                data[(base + filled) as usize] = (224 + (sub % 16)) as u8;
                data[(base + filled + 1) as usize] = (128 + (sub % 64)) as u8;
                data[(base + filled + 2) as usize] = (128 + (sub % 64)) as u8;
                filled += 3;
            } else {
                data[(base + filled) as usize] = (240 + (sub % 8)) as u8;
                data[(base + filled + 1) as usize] = (128 + (sub % 64)) as u8;
                data[(base + filled + 2) as usize] = (128 + (sub % 64)) as u8;
                data[(base + filled + 3) as usize] = (128 + (sub % 64)) as u8;
                filled += 4;
            }
        }
    }

    let mut sink: i64 = 0;
    for p in 0..passes {
        let idx = ((p * 40009) % total) as usize;
        data[idx] = (255 - (data[idx] as i64)) as u8;

        let mut count = 0i64;
        for rec in 0..records {
            if validate_window(&data, rec * w, w) {
                count += 1;
            }
        }
        sink += count;
    }
    println!("{}", sink);
}
