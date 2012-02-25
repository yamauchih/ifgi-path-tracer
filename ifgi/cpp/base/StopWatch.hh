//----------------------------------------------------------------------
// ifgi c++ implementation
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief stopwatch timer

#ifndef IFGI_CPP_BASE_STOPWATCH_HH
#define IFGI_CPP_BASE_STOPWATCH_HH

#include "types.hh"
#include "Exception.hh"

#include <sys/time.h>
#include <sstream>

namespace ifgi {
//----------------------------------------------------------------------
/// get current time as Float64 by gettimeofday().
/// \return current system time in second.
inline Float64 get_current_time()
{
    timeval tv;
    gettimeofday(&tv, 0);
    Float64 const cur_time
        = static_cast< Float64 >(tv.tv_sec) + (static_cast< Float64 >(tv.tv_usec) * 1.0e-6);
    return cur_time;
}

//----------------------------------------------------------------------
/// a stopwatch timer
class StopWatch
{
public:
    /// constructor
    StopWatch()
        :
        m_is_running(false),
        m_last_time(0.0),
        m_accumulated_time(0.0)
    {
        this->reset();
    }

    /// is this stopwatch running?
    /// \return true when running.
    bool is_run() const { return m_is_running; }

    /// run the stop watch. Exception when if the watch has already been run.
    void run()
    {
        if(this->is_run()){
            throw Exception("Cannot run the watch. The stopwatch is running.");
        }
        m_is_running = true;
        m_last_time = get_current_time();
    }

    /// stop the stopwatch. Exception, if the watch has already been stopped.
    void stop()
    {
        if(!this->is_run()){
            throw Exception("Cannot stop the watch. The stopwatch has been stopped.");
        }
        m_accumulated_time += get_current_time() - m_last_time;
        m_is_running = false;
    }

    /// reset the watch.
    void reset()
    {
        m_is_running = false;
        m_last_time        = 0.0;
        m_accumulated_time = 0.0;
    }

    /// give current time (in seconds). call only if watch is stopped.
    Float64 get_accumulated_time() const
    {
        if(this->is_run()){
            throw Exception("cannot get the accumulated time. The stopwatch is running.");
        }
        return m_accumulated_time;
    }

    /// get string representation of the stop watch in second.
    std::string to_string() const
    {
        std::ostringstream sstr;
        sstr << this->get_accumulated_time();
        return sstr.str();
    }

private:
    /// stop watch running state.
    bool m_is_running;
    /// last current time
    Float64 m_last_time;
    /// accumulated time
    Float64 m_accumulated_time;
};

//----------------------------------------------------------------------
/// ostream for Stopwatch
/// \param[in] os output stream
/// \param[in] sw stopwatch
inline std::ostream & operator<<(std::ostream & os, StopWatch const & sw)
{
    os << sw.to_string();
    return os;
}

//----------------------------------------------------------------------
} // namespace ifgi
#endif // #ifndef IFGI_CPP_BASE_STOPWATCH_HH
