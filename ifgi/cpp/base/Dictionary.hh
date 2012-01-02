//----------------------------------------------------------------------
// ifgi c++ implementation: Dictionary.hh
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief python dict like class
#ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_DICTIONARY_HH
#define IFGI_PATH_TRACER_IFGI_CPP_BASE_DICTIONARY_HH

#include <map>
#include <string>
#include <sstream>

#include "types.hh"
#include "Vector.hh"

namespace ifgi {

/// dictonary conversion functions namespace
namespace dictconv {

//======================================================================
// any value -> string conversion
//======================================================================
//----------------------------------------------------------------------
/// general dictionary value to string conversion template function.
/// However, supported types should be specialized.
///
/// \param[in] val value of type T
/// \return string representation of val
template < typename T >
std::string value_to_string(T const & val)
{
    std::ostringstream osstr;
    osstr << val;
    return osstr.str();
}

//----------------------------------------------------------------------
/// Float32_3 -> string conversion
/// \param[in] vec a vector of Float32_3
/// \return string representation of Float32_3
template <>
std::string value_to_string< Float32_3 >(Float32_3 const & vec);

//======================================================================
// string -> any value conversion
//======================================================================

//----------------------------------------------------------------------
/// general string to dictionary value conversion template function.
/// However, supported types should be specialized.
template < typename T >
T string_to_value(std::string const & str)
{
    T ret;
    std::ostringstream osstr;
    osstr >> ret;
    return ret;
}

//----------------------------------------------------------------------
/// string -> Float32_3 conversion
/// \param[in] vec_str vector value
/// \return converted Float32_3
template <>
Float32_3 string_to_value< Float32_3 >(std::string const & vec_str);

//----------------------------------------------------------------------
} // namespace dictconv


/// dictionary value. The entry of Dictionary.
///
/// This is a value and can be converted to many other types if
/// possible. This has a string to keep the value.
///
class Dictionary_value
{
public:
    /// constructor
    Dictionary_value();

    /// constructor with supported type
    ///
    /// \param[in] val type T value, T must be supported in the
    /// conversion functions.
    template < typename T >
    explicit Dictionary_value(T const & val);

    /// destructor
    virtual ~Dictionary_value();

private:
    /// value kept in a string
    std::string m_value;
};

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
    void insert(std::string const & key, Dictionary_value const & val);

    /// get the value as a string
    std::string get(std::string const & key,
                    std::string const & default_val = "") const;

    /// get the value
    template < typename T > T get(std::string const & key,
                                  std::string const & default_val = "") const
    {

    }

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
