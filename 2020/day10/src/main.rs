use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead, Error};

const AOCDEBUG: bool = false;

type AOCResult = std::result::Result<(), Error>;

struct AOCProcessor {
    input: String,
    input_vec: Vec<i32>,
    result_a: i64,
    result_b: i64,
}

impl AOCProcessor {
    pub fn new(input: String) -> AOCProcessor {
        AOCProcessor {
            input,
            input_vec: Vec::new(),
            result_a: 0,
            result_b: 0,
        }
    }

    pub fn process(&mut self) -> AOCResult {
        self.initialize();

        let _ = match File::open(&self.input) {
            Ok(file) => {
                for line in io::BufReader::new(file).lines() {
                    if let Ok(line) = line {
                        self.process_line(&line[..]);
                    }
                }
            }
            Err(error) => return Err(error),
        };

        self.finalize();

        Ok(())
    }

    pub fn initialize(&mut self) {
        self.input_vec.clear();
        // self.input_vec.push(0);
    }

    fn process_line(&mut self, line: &str) {
        if line.len() > 0 {
            let n = line.parse::<usize>().unwrap() as i32;
            self.input_vec.push(n);
        }
    }

    pub fn finalize(&mut self) {
        self.finalize_a();
        self.finalize_b();
    }

    fn finalize_a(&mut self) {
        let mut count_1 = 0;
        let mut count_3 = 0;
        let mut inputs = self.input_vec.clone();
        inputs.sort();

        if AOCDEBUG {
            println!("{:?}", inputs);
        }
        for i in 1..inputs.len() {
            let v0 = inputs.get(i - 1).unwrap();
            let v1 = inputs.get(i).unwrap();
            match v1 - v0 {
                1 => {
                    count_1 += 1;
                }
                3 => {
                    count_3 += 1;
                }
                _ => {}
            }
        }

        if AOCDEBUG {
            println!("count_1:{}", count_1);
            println!("count_3:{}", count_3);
        }
        self.result_a = (count_3 + 1) * (count_1 + 1);
        println!("result_a:{}", self.result_a);
    }

    fn finalize_b(&mut self) {
        let max_v = 3 + self.input_vec.iter().map(|x| *x).max().unwrap();
        let mut inputs: Vec<i32> = Vec::new();
        inputs.push(0);
        inputs.extend(&self.input_vec);
        inputs.push(max_v);
        inputs.sort();
        if AOCDEBUG {
            println!("{:?}", inputs);
        }

        let mut cache: HashMap<i32, i64> = HashMap::new();
        cache.insert(inputs[0], 1);
        cache.insert(inputs[1], 1);

        for idx in 2..inputs.len() {
            if AOCDEBUG {
                println!("idx:{}, len:{}", idx, cache.len());
                for e in cache.iter() {
                    println!("{:?}", e);
                }
            }

            let mut new_cache: HashMap<i32, i64> = HashMap::new();

            let vi = inputs[idx];
            let mut nvi = 0;
            for (k, v) in cache.iter() {
                let vk = *k;
                if vi - vk <= 3 {
                    nvi += *v;
                    new_cache.insert(vk, *v);
                }
            }
            if nvi > 0 {
                new_cache.insert(vi, nvi);
            }

            cache = new_cache;
            if AOCDEBUG {
                println!("idx:{}, len:{}", idx, cache.len());
            }
        }
        if AOCDEBUG {
            println!("cache:{:?}", cache);
        }
        if cache.contains_key(&max_v) {
            self.result_b = *cache.get(&max_v).unwrap();
        }

        println!("result_b:{}", self.result_b);
    }
}

fn main() {
    let mut processor = AOCProcessor::new(String::from("input.txt"));
    match processor.process() {
        Ok(()) => {
            println!("DONE");
        }
        Err(error) => {
            panic!("{:#?}", error);
        }
    }
}
