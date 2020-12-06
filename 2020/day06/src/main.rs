use std::fs::File;
use std::io::{self, BufRead};


fn char_to_index(c: char) -> i32 {
    c as i32 - 'a' as i32
}

fn main() {

    let file = match File::open("input.txt") {
        Ok(file) => file,
        Err(error) => panic!("{}", error)
    };

    let mut sum_part1 = 0;
    let mut sum_part2 = 0;

    let mut entry = vec![0; 26];
    let mut nlines = 0;

    for line in io::BufReader::new(file).lines() {
        if let Ok(line) = line {
            if line.len() > 0 {
                nlines += 1;
                for c in line.chars() {
                    let idx = char_to_index(c) as usize;
                    entry[idx] += 1;
                }
            } else {
                let v_p1 : i32 = entry.iter().map(|i| { if *i > 0 { 1 } else { 0 }}).sum();
                let v_p2 : i32 = entry.iter().map(|i| { if *i == nlines { 1 } else { 0 }}).sum();
                sum_part1 += v_p1;
                sum_part2 += v_p2;
                entry = vec![0; 26];
                nlines = 0;
            }
        }
    }
    if nlines > 0 {
        let v_p1 : i32 = entry.iter().map(|i| { if *i > 0 { 1 } else { 0 }}).sum();
        let v_p2 : i32 = entry.iter().map(|i| { if *i == nlines { 1 } else { 0 }}).sum();
        sum_part1 += v_p1;
        sum_part2 += v_p2;
    }

    println!("sum_part1={}", sum_part1);
    println!("sum_part2={}", sum_part2);
}
