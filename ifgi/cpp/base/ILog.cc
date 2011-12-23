//----------------------------------------------------------------------
// ifgi c++ implementation
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief ifgi logger

#include "ILog.hh"
#include <iostream>

namespace ifgi {
//----------------------------------------------------------------------
// singleton instance
ILog * ILog::P_ILog = 0;

//----------------------------------------------------------------------
// set output level
void ILog::set_output_level(Uint32 lv) throw (ifgi::Exception)
{
    std::string const eh = "ILog::set_output_level: ";

    if(lv >= ILog_COUNT){
        throw Exception(eh + "illegal output level");
    }
    m_outputlevel = lv;
}

//----------------------------------------------------------------------
// get output level
Uint32 ILog::get_output_level() const
{
    return m_outputlevel;
}

//----------------------------------------------------------------------
// output error message
void ILog::error(std::string const & mes) const
{
    if(m_outputlevel >= ILog_Error){
        this->out("error: " + mes);
    }
}

//----------------------------------------------------------------------
// output warning message
void ILog::warn(std::string const & mes) const
{
    if(m_outputlevel >= ILog_Warning){
        this->out("warn: " + mes);
    }
}

//----------------------------------------------------------------------
// output info message
void ILog::info(std::string const & mes) const
{
    if(m_outputlevel >= ILog_Info){
        this->out("info: " + mes);
    }
}

//----------------------------------------------------------------------
// output debug message
void ILog::debug(std::string const & mes) const
{
    if(m_outputlevel >= ILog_Debug){
        this->out("debug: " + mes);
    }
}

//----------------------------------------------------------------------
// output message
void ILog::out(std::string const & mes) const
{
    std::cout << mes;
}

//----------------------------------------------------------------------
} // namespace ifgi

