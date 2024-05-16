#!/bin/env python3

import argparse
import csv
import json
from pathlib import Path
import shutil

def generate_json(src_csv: Path, dst_dir: Path):
    if dst_dir.exists():
        shutil.rmtree(dst_dir)
    dst_dir.mkdir()

    json_dir = dst_dir.joinpath('codex', 'items')
    json_dir.mkdir(parents=True)
    with open(src_csv, 'r', newline='') as csvfile, \
        open(json_dir.joinpath('meta.json'), 'w') as jsonfile:
        reader = csv.DictReader(csvfile)
        output_dict = {}
        for row in reader:
            json_dir.joinpath(f'{row["id"]}').mkdir()
            with open(json_dir.joinpath(f'{row["id"]}', 'meta.json'), 'w') as f:
                output_dict[row['id']] = {
                    'boss': int(row['boss']),
                }
                json.dump(output_dict[row['id']], f)
        json.dump(output_dict, jsonfile)

def main():
    parser = argparse.ArgumentParser(description='build server')
    parser.add_argument('--src', default='data/BossScaleItems.csv')
    parser.add_argument('--dst', default='dist')
    parser.add_argument('--template', default='template/index.html')
    
    args = parser.parse_args()
    src, dst = Path(args.src), Path(args.dst)
    template_file = Path(args.template)
    generate_json(src_csv=src, dst_dir=dst)
    shutil.copy(template_file, dst.joinpath('index.html'))


if __name__ == '__main__':
    main()
