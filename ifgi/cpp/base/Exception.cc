//----------------------------------------------------------------------
// ifgi c++ implementation
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief ifgi exception class

#include "Exception.hh"

namespace ifgi {

//----------------------------------------------------------------------
// set reason message
Exception & Exception::set(std::string const & what)
{
    m_what = what;
    return *this;
}

//----------------------------------------------------------------------
// append reason message
Exception& Exception::append(std::string const & what)
{
    m_what += what;
    return *this;
}

//----------------------------------------------------------------------
} // namespace ifgi

