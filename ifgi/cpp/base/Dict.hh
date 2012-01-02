//----------------------------------------------------------------------
// ifgi c++ implementation: Dict.hh
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief python dict like class
#ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_DICT_HH
#define IFGI_PATH_TRACER_IFGI_CPP_BASE_DICT_HH

#include <map>
#include <string>
#include <sstream>

#include "types.hh"
#include "Vector.hh"

namespace ifgi {

/// dictonary conversion functions namespace
namespace dict_conv {

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
} // namespace dict_conv


/// dictionary value. The entry of Dict.
///
/// This is a value and can be converted to many other types if
/// possible. This has a string to keep the value.
///
class Dict_value
{
public:
    /// constructor
    Dict_value() :
        m_value_str("")
    {
        // empty
    }

    /// constructor with supported type
    ///
    /// \param[in] val type T value, T must be supported in the
    /// conversion functions.
    template < typename T >
    explicit Dict_value(T const & val) :
        m_value_str(dict_conv::value_to_string(val))
    {
        // empty
    }

    /// destructor
    virtual ~Dict_value()
    {
        // empty
    }

    /// get string representation
    /// \return string representation of the value
    std::string get_string() const
    {
        return m_value_str;
    }

    /// set string to Dict_value.
    /// \param[in] val value to set
    template < typename T >
    void set(T const & val) const
    {
        m_value_str = dict_conv::value_to_string< T >(val);
    }

    /// get type T value
    /// \return type T converted value
    template < typename T >
    T get() const
    {
        return dict_conv::string_to_value< T >(m_value_str);
    }

private:
    /// value kept in a string
    std::string m_value_str;
};

/// dictionary, key value map with type conversion
class Dict
{
public:
    /// dictionary implementation type.
    typedef std::map< std::string, Dict_value > Dict_map;
    /// STL like typedef. value_type
    typedef Dict_map::value_type     value_type;
    /// STL like typedef. const_iterator
    typedef Dict_map::const_iterator const_iterator;
    /// STL like typedef. iterator
    typedef Dict_map::iterator       iterator;

public:
    /// constructor
    Dict();

    /// destructor.
    virtual ~Dict();

    /// clear the dictionary
    void clear();

    /// is defined the key?
    bool is_defined(std::string const & key) const;

    /// insert key and value
    ///
    /// if the same key has already been stored, val will replace the
    /// old value.
    ///
    /// \param[in] key key of the dict
    /// \param[in] val value of the dict
    /// \return return.first is value, return.second is false when the
    /// key has already inserted. (Same as the STL associative map
    /// insert convention)
    std::pair< Dict_map::iterator, bool >
    insert(std::string const & key, Dict_value const & val);

    /// insert all entries
    // Sint32 insert_all(Dict const & di);NIN

    /// erase an ently by its key
    // void erase(std::string const & key);NIN

    /// empty?
    /// \return true when empty
    bool empty() const;

    /// size of dict
    /// \return number of dict entries
    size_t size() const;

    /// get the value
    ///
    /// \param[in] key key of the dict
    /// \param[in] default_val default value of the get, when not
    /// found in dict, this default_val is returned.
    /// \return return the value
    template < typename T >
    T get(std::string const & key,
          T const & default_val = T()) const
    {
        Dict_map::const_iterator ci = m_dict_impl.find(key);
        if(ci != m_dict_impl.end()){
            return ci->second.get< T >();
        }
        return default_val;
    }

    /// set the value
    ///
    /// \param[in] key key of the dict
    /// \param[in] val value to be set. When the same key exists,
    /// override the value.
    template < typename T >
    void set(std::string const & key,
             T const & val)
    {
        this->insert(key, Dict_value(val));
    }

    /// output parameters to a stream.
    /// format: <line_prefix><key> = <value>
    // void write(std::ostream &os, std::string const & prefix) const; NIN

    /// read dictionary from a stream
    // void read(std::istream & is, std::string const & prefix);

private:
    /// dictionary implementation
    Dict_map m_dict_impl;
};

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_DICT_HH
