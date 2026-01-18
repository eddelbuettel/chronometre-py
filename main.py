#!/usr/bin/env python3

import chronometre

def main():
    s = chronometre.Stopwatch()
    print(s)
    print(s.elapsed())

    s2 = chronometre.bake(s)
    print(s2)
    print(s2.elapsed())

if __name__ == "__main__":
    main()
