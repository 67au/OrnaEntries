#!/bin/env python3

import argparse
import csv
import io
from pathlib import Path


def merge(item_list_txt: Path, boss_scale_csv: Path):
    fieldnames = ['id', 'boss']

    with open(boss_scale_csv, 'r+', newline='') as csvfile, \
            open(item_list_txt, 'r') as txtfile:
        tmpfile = io.StringIO()
        boss_dict = {}
        reader = csv.DictReader(csvfile)
        for row in reader:
            boss_dict[row['id']] = row['boss']
        for line in iter(txtfile.readline, ''):
            id = line.strip()
            if id not in boss_dict:
                boss_dict[id] = 0
        writer = csv.DictWriter(tmpfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(
            {'id': key, 'boss': boss_dict[key]} for key in sorted(boss_dict.keys())
        )

        csvfile.seek(0)
        csvfile.truncate()
        csvfile.write(tmpfile.getvalue())


def main():
    parser = argparse.ArgumentParser(description='merge2csv')
    parser.add_argument('--src', default='data/ItemList.txt')
    parser.add_argument('--dst', default='data/BossScaleItems.csv')

    args = parser.parse_args()
    src = Path(args.src)
    dst = Path(args.dst)
    print(f'Merge {src} into {dst}')

    merge(
        item_list_txt=src,
        boss_scale_csv=dst,
    )

if __name__ == '__main__':
    main()
