//----------------------------------------------------------------------
// ifgi c++ implementation: Dictionary.hh
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief python dict like class
#ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_DICTIONARY_HH
#define IFGI_PATH_TRACER_IFGI_CPP_BASE_DICTIONARY_HH

#include <map>
#include <vector>
#include <string>
#include <sstream>

#include "types.hh"
#include "Vector.hh"

namespace ifgi {

/// dictonary conversion functions namespace
namespace dictionary_conv {

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
/// string -> string conversion (or no conversion)
/// \param[in] str a string
/// \return a string
template <>
std::string value_to_string< std::string >(std::string const & str);

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
    std::istringstream isstr(str);
    isstr >> ret;
    return ret;
}

//----------------------------------------------------------------------
/// string -> string conversion (or no conversion)
/// \param[in] str a string
/// \return a string
template <>
std::string string_to_value< std::string >(std::string const & str);

//----------------------------------------------------------------------
/// string -> Float32_3 conversion
/// \param[in] vec_str vector value
/// \return converted Float32_3
template <>
Float32_3 string_to_value< Float32_3 >(std::string const & vec_str);

//----------------------------------------------------------------------
} // namespace dictionary_conv


/// dictionary value. The entry of Dictionary.
///
/// This is a value and can be converted to many other types if
/// possible. This has a string to keep the value.
///
class Dictionary_value
{
public:
    /// constructor
    Dictionary_value() :
        m_value_str("")
    {
        // empty
    }

    /// constructor with supported type
    ///
    /// \param[in] val type T value, T must be supported in the
    /// conversion functions.
    template < typename T >
    explicit Dictionary_value(T const & val) :
        m_value_str(dictionary_conv::value_to_string(val))
    {
        // empty
    }

    /// destructor
    virtual ~Dictionary_value()
    {
        // empty
    }

    /// get string representation
    /// \return string representation of the value
    std::string get_string() const
    {
        return m_value_str;
    }

    /// set string to Dictionary_value.
    /// \param[in] val value to set
    template < typename T >
    void set(T const & val) const
    {
        m_value_str = dictionary_conv::value_to_string< T >(val);
    }

    /// get type T value
    /// \return type T converted value
    template < typename T >
    T get() const
    {
        return dictionary_conv::string_to_value< T >(m_value_str);
    }

private:
    /// value kept in a string
    std::string m_value_str;
};

/// dictionary, key value map with type conversion
class Dictionary
{
public:
    /// dictionary implementation type.
    typedef std::map< std::string, Dictionary_value > Dictionary_map;
    /// STL like typedef. value_type
    typedef Dictionary_map::value_type     value_type;
    /// STL like typedef. const_iterator
    typedef Dictionary_map::const_iterator const_iterator;
    /// STL like typedef. iterator
    typedef Dictionary_map::iterator       iterator;

public:
    /// constructor
    Dictionary();

    /// destructor.
    virtual ~Dictionary();

    /// copy constructor
    /// \param[in] rhs right hand side, copy source
    Dictionary(Dictionary const & rhs);

    /// operator=
    /// \param[in] rhs right hand side, copy source
    Dictionary const & operator=(Dictionary const & rhs);

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
    std::pair< Dictionary_map::iterator, bool >
    insert(std::string const & key, Dictionary_value const & val);

    /// insert all entries. The existing entry will be overwritten, if
    /// there is no overwritten, they remains. If you want to set
    /// it, first clear() the dictionary and insert_all().
    ///
    /// \param[in] dict dictionary to be inserted.
    /// \return number of inserted entries
    Sint32 insert_all(Dictionary const & dict);

    /// erase an ently by its key. If no key in the dictionary, no
    /// effect.
    ///
    /// \param[in] key key of erasing entry
    /// \return true when erase the entry with the key
    bool erase(std::string const & key);

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
        Dictionary_map::const_iterator ci = m_dict_impl.find(key);
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
        this->insert(key, Dictionary_value(val));
    }

    /// const_iterator begin()
    /// \return the first element of Dictionary_value
    const_iterator begin() const;

    /// const_iterator end()
    /// \return the one past end of elements of Dictionary_value
    const_iterator end() const;

    /// output parameters to a stream.
    /// format: <line_prefix><key> = <value>
    ///
    /// \param[in] os output stream
    /// \param[in] perfix prefix string to add
    void write(std::ostream &os,
               std::string const & prefix = std::string("")) const;

    /// read dictionary from a stream
    // void read(std::istream & is, std::string const & prefix);

private:
    /// implementation of dictionary
    Dictionary_map m_dict_impl;
};

//----------------------------------------------------------------------
/// is all keys are defined in the dictionary?
///
/// \param[in] dict   dictionary to be checked
/// \param[in] keyvec a vector of keys
/// \param[out] p_non_def_key_vec (output) not defined keys vector,
/// when 0, no output
/// \return true if all keys are defined.
extern bool is_all_key_defined(Dictionary const & dict,
                               std::vector< std::string > const & keyvec,
                               std::vector< std::string > * p_non_def_key_vec = 0);

//----------------------------------------------------------------------
/// is all keys are defined in the dictionary? This calls overloaded
/// function (2nd arg is std::vector).
///
/// \code
/// char const * p_key[] = {"key0", "key1", 0 };
/// bool r = is_all_key_defined(dict, p_key, p_nondefs);
/// \endcode
///
/// \param[in] dict   dictionary to be checked
/// \param[in] p_keyarry an char* array of keys. The array should be 0
/// terminated.
/// \param[out] p_non_def_key_vec (output) not defined keys vector,
/// when 0, no output
/// \return true if all keys are defined.
extern bool is_all_key_defined(Dictionary const & dict,
                               char const * p_keyarray[],
                               std::vector< std::string > * p_non_def_key_vec = 0);
//----------------------------------------------------------------------
} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_DICTIONARY_HH

