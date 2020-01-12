# -*- coding: utf-8 -*-


def countAndSay(n: int) -> str:
    if not (1 <= n <= 30):
        return ''
    strs = '1'
    for i in range(n - 1):
        num = 1
        ls = tag = ''
        for ch in range(len(strs)):
            if tag is not strs[ch]:
                tag = strs[ch]
                num = 1
                lo = str(num) + tag
            else:
                num += 1
                lo = str(num) + tag

            if len(strs) - 1 == ch or tag is not strs[ch + 1]:
                ls += lo
        strs = ls
    return strs


if __name__ == '__main__':
    print(countAndSay(1))
    pass
