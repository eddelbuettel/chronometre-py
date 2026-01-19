#include <pybind11/pybind11.h>
#include <pybind11/chrono.h>

// Inspired by an existing class 'stopwatch' in spdlog
// but removing ftm header and compacted for the example use here

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
private:
    // internal state variable of clock time point 'when started'
    std::chrono::time_point<std::chrono::steady_clock> start_tp_;

    // Static factory function returning a raw pointer
    static stopwatch* create_ptr(stopwatch& obj, std::string& s) {
        auto p = static_cast<stopwatch*>( (void*) strtol(s.c_str(), nullptr, 0));
        p->start_tp_ = obj.start_tp_;
        return p;
    }

public:
    // default constructor initialising stopwatch as of 'right now'
    stopwatch() : start_tp_{std::chrono::steady_clock::now()} {}

    // Added constructor from string which is used to receive the _address_ of another
    // instance from which the value of the one member variable 'start_tp_' is copied
    // This is usable from R in the context of this example, but is not advised from
    // Python due to object lifetime considerations; we may need a static factory function
    stopwatch(std::string& s) {
        auto sp = static_cast<stopwatch*>( (void*) strtol(s.c_str(), nullptr, 0) );
        start_tp_ = sp->start_tp_;
    }

    // standard accessor to determine elapsed time in seconds as duration object
    // add .count() to convert to to double instead of duration object (which has formating)
    std::chrono::duration<double> elapsed() const {
        return std::chrono::duration<double>(std::chrono::steady_clock::now() - start_tp_);
    }

    // helper to reset internal clock to current time
    void reset() {
        start_tp_ = std::chrono::steady_clock::now();
    }

    // let bake have access to private member elements
    friend stopwatch& bake(stopwatch&);

};

stopwatch& bake(stopwatch& sw) {
    std::stringstream ss;
    ss << std::showbase << std::hex << reinterpret_cast<void*>(&sw);
    std::string hex_address{ss.str()};
    return *stopwatch::create_ptr(sw, hex_address);
}

// Standard pybind11 wrapping of C++ class 'stopwatch' into a module 'Stopwatch'
// exported by this 'chronometre' Python package. The second constructor can be
// used to pass a pointer to an existing instance (as a string containing the address)
// Note that this works from R but not from Python; we can use the factory function
// there
PYBIND11_MODULE(_chronometre, m) {
    pybind11::class_<stopwatch>(m, "Stopwatch")
        .def(pybind11::init<>())
        .def(pybind11::init<std::string&>())
        .def("elapsed", &stopwatch::elapsed)
        .def("reset", &stopwatch::reset);

    m.def("bake", &bake, "Return a cloned stopwatch", pybind11::arg("sw"));
}
