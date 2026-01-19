#!/usr/bin/env python3

import chronometre
import time

def main():
    s = chronometre.Stopwatch()
    print(s)
    print(s.elapsed())
    time.sleep(0.1)
    print(s.elapsed())

    s2 = chronometre.bake(s)
    print(s2)
    print(s2.elapsed())
    time.sleep(0.1)
    print(s2.elapsed())

    print(s.elapsed())

if __name__ == "__main__":
    main()
