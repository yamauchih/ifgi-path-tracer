//----------------------------------------------------------------------
// ifgi c++ implementation: Dictionary.hh
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief key value map with type conversion
#ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_DICTIONARY_HH
#define IFGI_PATH_TRACER_IFGI_CPP_BASE_DICTIONARY_HH

#include <map>
#include <string>
// #include <iostream>

namespace ifgi {

/// value string. The entry of Dictionary.
///
/// This is a value and can be converted to many other type if
/// possible. This has a string to keep the value.
///
// class ValueString
// {
// public:
//     /// constructor
//     ValueString();
//     /// destructor
//     virtual ~ValueString();

// private:
//     /// value kept in a string
//     std::string m_value;
// };

/// dictionary, key value map with type conversion
class Dictionary
{
public:
    /// 
    typedef std::map< std::string, std::string > Dictionary_map;

public:
    /// constructor
    Dictionary();

    /// destructor.
    virtual ~Dictionary();

    /// clear the dictionary
    void clear();

    /// is defined the key?
    bool is_defined(std::string const & key) const;

    /// insert key and value
    /// pair<iterator, bool>
    void insert(std::string const & key, std::string const & val);

    /// get the value as a string
    std::string get(std::string const & key,
                    std::string const & default_val = "") const;

    /// get the value
    // template < typename T > T get(std::string const & key,
    //                               std::string const & default_val = "") const ;

    // /// output parameters to stream, format: <line_prefix><key> = <value>
    // void write(std::ostream &os, std::string const & prefix) const;

    // /// read dictionary from a stream
    // void read(std::istream & is, std::string const & prefix);

private:
    /// dictionary implementation
    Dictionary_map m_dict_impl;
};

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_DICTIONARY_HH
