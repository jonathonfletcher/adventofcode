use std::collections::{HashMap, HashSet};
use std::fs::File;
use std::io::{self, BufRead, Error};

const AOCDEBUG: bool = false;

type AOCResult = std::result::Result<(), Error>;

#[derive(Hash, Eq, PartialEq, Debug)]
struct BagCounter {
    bag_type: String,
    bag_count: usize,
}

struct AOCProcessor {
    input: String,
    bag_nesting_map: HashMap<String, Vec<String>>,
    bag_container_map: HashMap<String, Vec<BagCounter>>,
    result_a: usize,
    result_b: usize,
}

impl AOCProcessor {
    pub fn new(input: String) -> AOCProcessor {
        AOCProcessor {
            input,
            bag_nesting_map: HashMap::new(),
            bag_container_map: HashMap::new(),
            result_a: 0,
            result_b: 0,
        }
    }

    pub fn process(&mut self) -> AOCResult {
        let file = match File::open(&self.input) {
            Ok(file) => file,
            Err(error) => return Err(error),
        };

        self.initialize();
        for line in io::BufReader::new(file).lines() {
            if let Ok(line) = line {
                self.process_line(&line[..]);
            }
        }
        self.finalize();

        Ok(())
    }

    pub fn initialize(&mut self) {
        self.bag_nesting_map.clear();
        self.bag_container_map.clear();
    }

    fn process_line(&mut self, line: &str) {
        let mut parse_stack: Vec<String> = Vec::new();

        if line.len() > 0 {
            if AOCDEBUG {
                println!("{:?}", line);
            }

            let tokens: Vec<&str> = line.split_ascii_whitespace().collect();
            let mut skip = false;
            let mut outside_bag_type: String = String::from("");
            for t in tokens {
                if skip {
                    break;
                }
                if t.eq("no") {
                    skip = true;
                } else if t.eq("contain") {
                    let _ = parse_stack.pop().unwrap();
                    let bag_color = parse_stack.pop().unwrap();
                    let bag_adjective = parse_stack.pop().unwrap();

                    outside_bag_type = format!("{} {}", bag_adjective, bag_color);

                    self.bag_container_map
                        .insert(outside_bag_type.clone(), Vec::new());
                } else if t.eq("bag,") || t.eq("bags,") || t.eq("bag.") || t.eq("bags.") {
                    let bag_color = parse_stack.pop().unwrap();
                    let bag_adjective = parse_stack.pop().unwrap();
                    let bag_count = parse_stack.pop().unwrap();

                    let bag_type = format!("{} {}", bag_adjective, bag_color);
                    let bag_count = bag_count.parse::<usize>().unwrap();

                    if !self.bag_nesting_map.contains_key(&bag_type.clone()) {
                        self.bag_nesting_map.insert(bag_type.clone(), Vec::new());
                    }
                    if let Some(x) = self.bag_nesting_map.get_mut(&bag_type.clone()) {
                        x.push(outside_bag_type.clone());
                    }

                    if let Some(x) = self.bag_container_map.get_mut(&outside_bag_type) {
                        x.push(BagCounter {
                            bag_type,
                            bag_count,
                        });
                    }
                } else {
                    parse_stack.push(String::from(t));
                }
            }
        }
    }

    pub fn finalize(&mut self) {
        self.finalize_a();
        self.finalize_b();
    }

    fn finalize_a(&mut self) {
        fn f(
            searchlist: &Vec<String>,
            map: &HashMap<String, Vec<String>>,
            ignoreset: &mut HashSet<String>,
            indent: usize,
        ) -> usize {
            let mut count = 0;
            for e in searchlist.iter() {
                if !ignoreset.contains(e) {
                    ignoreset.insert(e.clone());
                    count += 1;

                    if let Some(x) = map.get(e) {
                        if AOCDEBUG {
                            let mut indent_string = String::from("");
                            for _ in 0..=indent {
                                indent_string.push(' ');
                            }
                            println!("{}e:{:?} -> x[{}]:{:?}", indent_string, e, x.len(), x);
                        }
                        count += f(x, map, ignoreset, indent + 1);
                    }
                }
            }
            count
        }

        let mut searchlist: Vec<String> = Vec::new();
        let mut ignoreset: HashSet<String> = HashSet::new();

        searchlist.push(String::from("shiny gold"));

        let count = f(&searchlist, &self.bag_nesting_map, &mut ignoreset, 0);
        if AOCDEBUG {
            println!("count:{}", count);
            println!("ignoreset.len:{}", ignoreset.len());
        }
        if ignoreset.len() > 0 {
            self.result_a = ignoreset.len() - 1;
        }
    }

    fn finalize_b(&mut self) {
        fn f(
            searchstring: &String,
            map: &HashMap<String, Vec<BagCounter>>,
            indent: usize,
        ) -> usize {
            let mut count = 0;
            if let Some(contents) = map.get(searchstring) {
                if AOCDEBUG {
                    let mut indent_string = String::from("");
                    for _ in 0..=indent {
                        indent_string.push(' ');
                    }
                    println!(
                        "{}{:?} -> [{}]:{:?}",
                        indent_string,
                        searchstring,
                        contents.len(),
                        contents
                    );
                }

                for e in contents.iter() {
                    count += e.bag_count + e.bag_count * f(&e.bag_type, map, indent + 1);
                }
            }
            count
        }

        let searchstring: String = String::from("shiny gold");
        self.result_b = f(&searchstring, &self.bag_container_map, 0);
    }
}

fn main() {
    let mut p = AOCProcessor::new(String::from("input.txt"));

    match p.process() {
        Ok(()) => {
            println!("result_a: {}", p.result_a);
            println!("result_b: {}", p.result_b);
            println!("DONE");
        }
        Err(error) => {
            panic!("{:#?}", error);
        }
    }
}
