#include <pybind11/pybind11.h>
#include <pybind11/chrono.h>

// Inspired by an existing class 'stopwatch' in spdlog
// but removing ftm header and compacted for example here

// Copyright(c) 2015-present, Gabi Melman & spdlog contributors.
// Distributed under the MIT License (http://opensource.org/licenses/MIT)
//
// Stopwatch support for spdlog  (using std::chrono::steady_clock).
// Displays elapsed seconds since construction as double.
//
// Usage:
//
// spdlog::stopwatch sw;
// ...
// spdlog::debug("Elapsed: {} seconds", sw);    =>  "Elapsed 0.005116733
// seconds" spdlog::info("Elapsed: {:.6} seconds", sw);  =>  "Elapsed 0.005163
// seconds"
//
//
// If other units are needed (e.g. millis instead of double), include
// "fmt/chrono.h" and use "duration_cast<..>(sw.elapsed())":
//
// #include <spdlog/fmt/chrono.h>
//..
// using std::chrono::duration_cast;
// using std::chrono::milliseconds;
// spdlog::info("Elapsed {}", duration_cast<milliseconds>(sw.elapsed())); =>
// "Elapsed 5ms"

class stopwatch {
    std::chrono::time_point<std::chrono::steady_clock> start_tp_;
public:
    stopwatch() : start_tp_{std::chrono::steady_clock::now()} {}
    stopwatch(std::string& s) {
        auto sp = static_cast<stopwatch*>( (void*) strtol(s.c_str(), nullptr, 0) );
        start_tp_ = sp->start_tp_;
    }
    std::chrono::duration<double> elapsed() const {
        return std::chrono::duration<double>(std::chrono::steady_clock::now() - start_tp_);
    }
    void reset() {
        start_tp_ = std::chrono::steady_clock::now();
    }
};

PYBIND11_MODULE(chronometre, m) {
    pybind11::class_<stopwatch>(m, "Stopwatch")
        .def(pybind11::init<>())
        .def(pybind11::init<std::string&>())
        .def("elapsed", &stopwatch::elapsed)
        .def("reset", &stopwatch::reset);
}
