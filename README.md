
## chronometre: Simple Stopwatch Class

[![ci](https://github.com/eddelbuettel/chronometre-py/actions/workflows/ci.yaml/badge.svg)](https://github.com/eddelbuettel/chronometre-py/actions/workflows/ci.yaml)

### Motivation

Interacting with Python code from R has become very convenient via the [reticulate][reticulate]
package which also takes care of most standard data types used by R users.  On top of that, [arrow][arrow]
facilitates exchange of vectors and especially data.frame (or in its parlance RecordBatch)
objects. Using [nanoarrow][nanoarrow] to do so takes the (considerable) pain of building with arrow
away.

But sometimes we want bespoke custom objects from a specific library. R does well with external
pointer objects, so a recent question in the [Rcpp][rcpp] context was: how do we do this with
Python?

This repository has one answer and working demonstration. It uses a very small but clever class: a
'stopwatch' implementation taken (with loving appreciation and a nod) from the lovely
[spdlog][spdlog] library, and specifically the already simplified version in
[RcppSpdlog][rcppspdlog] presented by [this 'spdlog_stopwatch.h' file][spdlog_stopwatch].

It is used by the demo in the sibbling repository [chronometre-r][chronometre-r].

### Python Demo

So once installed this minimal demo in `main.py` does this:

```py
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
```

It allocates a stopwatch object, and then 'clones' it via a helper function into a second object
_still pointing at the same memory location_ and hence sharing the object.  (From R we can also
use an additional constructor, but when we use that from Python 'lifetime' behavior gets in the way;
the factory helper function gets around that. A small nuance.)

This generated sample output such as the following:

```sh
(chronometre) $ ./main.py
<chronometre._chronometre.Stopwatch object at 0x7ba8071abc70>
0:00:00.000016
0:00:00.100226
<chronometre._chronometre.Stopwatch object at 0x7ba8071abc70>
0:00:00.100287
0:00:00.200371
0:00:00.200408
(chronometre) $
```

demonstrating that the memory address is in fact the same, and the behavior is shared.

### Author

Dirk Eddelbuettel for the sample Python package

Gabi Melman for the initial stopwatch class

### License

The package as a whole is licensed under the GPL (version 2 or later).

The stopwatch C++ class by Gabi Melman is MIT licensed.


[reticulate]: https://github.com/rstudio/reticulate
[arrow]: https://arrow.apache.org/
[nanoarrow]: https://github.com/apache/arrow-nanoarrow
[rcpp]: https://www.rcpp.org
[spdlog]: https://github.com/gabime/spdlog
[rcppspdlog]: https://github.com/eddelbuettel/rcppspdlog
[spdlog_stopwatch]: https://github.com/eddelbuettel/rcppspdlog/blob/master/inst/include/spdlog_stopwatch.h
[chronometre-r]: https://github.com/eddelbuettel/chronometre-r
