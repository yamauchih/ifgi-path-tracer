//----------------------------------------------------------------------
// ifgi c++ implementation
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief ifgi logger

#ifndef IFGI_CPP_BASE_ILOG_HH
#define IFGI_CPP_BASE_ILOG_HH

#include "types.hh"
#include "Exception.hh"

namespace ifgi {

/// ifgi simple logger class
class ILog
{
public:
    /// log level
    enum ILog_loglevel_e {
        /// error
        ILog_Error,
        /// warning
        ILog_Warning,
        /// info
        ILog_Info,
        /// debug
        ILog_Debug,
        /// sentinel
        ILog_COUNT
    };

public:
    /// get instance for the singleton.
    static ILog * instance()
    {
        if(P_ILog == 0)
        {
            P_ILog = new ILog();
        }
        return P_ILog;
    }

private:
    /// singleton instance
    static ILog * P_ILog;


public:
    /// set output level
    ///
    /// Output level:
    /// - ILog_Error
    /// - ILog_Warning
    /// - ILog_Info
    /// - ILog_Debug
    ///
    /// \param[in] _lv output level
    void set_output_level(Uint32 lv) throw (ifgi::Exception);

    /// get output level
    /// \return current output level
    Uint32 get_output_level() const;

    /// output error message
    /// \param[in] mes message
    void error(std::string const & mes) const;

    /// output warning message
    /// \param[in] mes message
    void warn(std::string const & mes) const;

    /// output info message
    /// \param[in] mes info message
    void info(std::string const & mes) const;

    /// output debug message
    /// \param[in] mes message
    void debug(std::string const & mes) const;

    /// output message
    /// \param[in] mes message
    void out(std::string const & mes) const;


private:
    /// default constructor
    ILog() :
        m_outputlevel(ILog_Info)
    {
        // empty
    }

private:
    /// current output level
    Uint32 m_outputlevel;

private:
    /// copy constructor, never used.
    ILog(const ILog& _rhs);
    /// operator=, never used.
    const ILog& operator=(const ILog& _rhs);
};

} // namespace ifgi
#endif // #ifndef IFGI_CPP_BASE_ILOG_HH
