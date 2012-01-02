//----------------------------------------------------------------------
// ifgi c++ implementation: Dictionary.hh
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief key value map with type conversion

#include "Dictionary.hh"
#include "Exception.hh"

namespace ifgi {

//======================================================================
// any value -> string conversion
//======================================================================

// dictonary conversion functions namespace
namespace dictconv {

/// general vector to string method
/// \param[val] vec_val vector value
/// \return string representation of vec_val
template < typename T, int DIM >
static inline std::string vector_value_to_string(
    Vector< T, DIM > const & vec_val)
{
    std::ostringstream osstr;
    for(int i = 0; i < (vec_val.dim() - 1); ++i){
        osstr << vec_val[i] << " ";
    }
    osstr << vec_val[vec_val.dim() - 1];
    return osstr.str();
}

//----------------------------------------------------------------------
// Float32_3 -> string conversion
template <>
std::string value_to_string< Float32_3 >(Float32_3 const & vec)
{
    return vector_value_to_string< Float32, 3 >(vec);
}

//======================================================================
// string -> any value conversion
//======================================================================

/// general string to vector conversion method
///
/// throw an Exception when conversion failed.
///
/// \param[in] vec_str vector string
/// \return type vector representation of vec_str

#define IFGI_MAKE_STRING_FROM_SYMBOL_X(s) IFGI_MAKE_STRING_FROM_SYMBOL(s)
#define IFGI_MAKE_STRING_FROM_SYMBOL(s) #s

template < typename T, int DIM >
static inline Vector< T, DIM > string_to_vector_value(
    std::string const & vec_str) 
{
    Vector< T, DIM > ret;
    std::istringstream isstr(vec_str);
    for(int i = 0; i < ret.dim(); ++i){
        isstr >> ret[i];
        if(isstr.fail()){
            std::stringstream sstr;
            sstr << "failed string to vector conversion. ["
                 << vec_str + "] to Vector< "
                 << std::string(IFGI_MAKE_STRING_FROM_SYMBOL_X(T)) << ", "
                 << DIM << " >.";
            throw Exception(sstr.str());
        }
    }
    return ret;
}

#undef IFGI_MAKE_STRING_FROM_SYMBOL_X
#undef IFGI_MAKE_STRING_FROM_SYMBOL

//----------------------------------------------------------------------
// string -> Float32_3 conversion
template <>
Float32_3 string_to_value< Float32_3 >(std::string const & val_str)
{
    Float32_3 const ret = string_to_vector_value< Float32, 3 >(val_str);
    return ret;
}

//----------------------------------------------------------------------
} // namespace dictconv


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

