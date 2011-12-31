//----------------------------------------------------------------------
// ifgi c++ implementation: Dictionary.hh
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief key value map with type conversion

#include "Dictionary.hh"

namespace ifgi {

//----------------------------------------------------------------------
// constructor
Dictionary::Dictionary()
{
    // empty
}

//----------------------------------------------------------------------
// destructor.
Dictionary::~Dictionary()
{
    // empty
}

//----------------------------------------------------------------------
// clear the dictionary
void Dictionary::clear()
{
    m_dict_impl.clear();
}

//----------------------------------------------------------------------
// is defined the key?
bool Dictionary::is_defined(std::string const & key) const
{
    Dictionary_map::const_iterator di = m_dict_impl.find(key);
    if(di != m_dict_impl.end()){
        return true;
    }
    return false;
}

//----------------------------------------------------------------------
// insert key and value
void Dictionary::insert(std::string const & key, std::string const & val)
{
    m_dict_impl.insert(std::make_pair(key, val));
}

//----------------------------------------------------------------------
// get the value as a string
std::string Dictionary::get(std::string const & key,
                            std::string const & default_val) const
{
    Dictionary_map::const_iterator di = m_dict_impl.find(key);
    if(di != m_dict_impl.end()){
        return di->second;
    }
    return default_val;
}

//----------------------------------------------------------------------
// get the value
// template < typename T > T Dictionary::get(std::string const & key,
//                                           std::string const & default_val = "");

//----------------------------------------------------------------------
// output parameters to stream, format: <line_prefix><key> = <value>
// void Dictionary::write(std::ostream &os, std::string const & prefix) const;

//----------------------------------------------------------------------
// read dictionary from a stream
// void Dictionary::read(std::istream & is, std::string const & prefix);

//----------------------------------------------------------------------
} // namespace ifgi

