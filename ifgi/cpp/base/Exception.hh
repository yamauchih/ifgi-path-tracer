//----------------------------------------------------------------------
// ifgi c++ implementation
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief ifgi exception class

#ifndef IFGI_CPP_BASE_EXCEPTION_HH
#define IFGI_CPP_BASE_EXCEPTION_HH

#include <string>
#include <stdexcept>

namespace ifgi {

/// \defgroup ifgi base facilities.

/// Exception
/// \ingroup ifgi_base
///
/// Note: exception can not handled accross different shared objects,
/// therefore should not be inlined.
///
class Exception : public std::exception
{
public:
    /// Constructor
    /// \param[in] what the reason of exception
    Exception(std::string const & what) throw() : m_what(what)
    {
        // empty
    }
    /// destructor
    virtual ~Exception() throw()
    {
        // empty
    }
    /// get exception reason
    virtual const char * what() const throw(){ return m_what.c_str(); }
    /// set reason message
    /// \param[in] what exception reason
    Exception& set(std::string const & what);
    /// append reason message
    /// \param[in] what exception reason
    Exception& append(std::string const & what);
private:
    /// the exception message
    std::string m_what;
};

} // namespace ifgi
#endif // #ifndef IFGI_CPP_BASE_EXCEPTION_HH
