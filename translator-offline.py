#!/usr/bin/env python3
import requests
import os
from os.path import dirname, realpath
import sys
import pandas as pd

def main():
    # 读取xlsx文件中名为'sheet_name'的sheet
    excel_name = sys.argv[1] if len(sys.argv) > 1 else 'THOL Translation.xlsx'
    sheet_name = 'Elife'
    langs = ['key', 'English', 'Chinese']

    # 读取表
    print(f'reading {excel_name}')
    df = pd.read_excel(excel_name, sheet_name=sheet_name, dtype=str)

    # 选择语言
    print(f'Target language: ')
    for i in range(1, len(langs)):
        print(f'{i}: {langs[i]}')
    print(f'Please input 1~{len(langs)-1}: ')
    while 1:
        try:
            lang = int(input())
            if lang < 1 or lang > len(langs)-1:
                raise ValueError
            break
        except ValueError:
            print(f'Please input 1~{len(langs)-1}: ')

    # 是否追加中文
    print('\nAppend English after translated objects?')
    print('0: No')
    print('1: Yes')
    print('Please input 0/1: ')
    while 1:
        try:
            is_append = int(input())
            if is_append < 0 or is_append > 1:
                raise ValueError
            break
        except ValueError:
            print('Please input 0/1: ')

    # 翻译
    print("Translating Objects...")

    if os.path.isfile('objects/cache.fcz'):
        os.remove('objects/cache.fcz')

    keys = df['key'].fillna('') # 将NaN替换为空字符串
    data1 = df.iloc[:, lang].fillna('') # 目标语言
    if is_append:
        data2 = df['English'].fillna('') # 追加中文
    print(len(keys))
    for i in range(len(keys)):
        translated = data1[i]
        if not pd.isna(translated):
            translated = translated.strip()
            try:
                with open(f'objects/{keys[i]}.txt', encoding='utf-8') as f:
                    content = f.readlines()
            except Exception as e:
                continue
            if is_append:
                data2_append = data2[i].strip()
                utf8_data2_append = data2_append.encode('utf8')
                # 如果中文列是空的, 可以追加带有中文的英文; 如果中文列有数据, 那么不追加带有中文的英文
                if len(data2_append) != len(utf8_data2_append):
                    data2_append = ''
                content[1] = translated.split('#')[0].split('$')[0].split('@')[0] + data2_append + '\n'
            elif translated != '':
                content[1] = translated + '\n'
            with open(f'objects/{keys[i]}.txt', 'w', encoding='utf-8') as f:
                f.writelines(content)

    menuItems = {}
    try:
        with open('languages/English.txt', encoding='utf-8') as f:
            datas = f.readlines()
            for data in datas:
                if data == '\n':
                    continue
                name = data.split(' ')[0]
                value = data[data.index('"') + 1:-2]
                menuItems[name] = value

    except FileNotFoundError as e:
        print(e)

    print("Translating Menu...")

    df = pd.read_excel(excel_name, sheet_name='Menu', dtype=str)
    keys = df['Key'].dropna()
    data = df.iloc[:, 3*lang]
    for i in range(len(keys)):
        if not pd.isna(data[i]):
            menuItems[keys[i]] = data[i]

    with open('languages/English.txt', 'w', encoding='utf-8') as f:
        for key in menuItems:
            f.write(f'{key} "{menuItems[key]}"\n')

    print("Translating done!")


if __name__ == '__main__':
    main()
