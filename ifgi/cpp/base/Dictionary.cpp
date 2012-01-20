//----------------------------------------------------------------------
// ifgi c++ implementation: Dictionary.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief key value map with type conversion

#include "Dictionary.hh"
#include "Exception.hh"

#include <algorithm>

namespace ifgi {

//======================================================================
// any value -> string conversion
//======================================================================

// dictonary conversion functions namespace
namespace dictionary_conv {

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
// string -> string conversion (or no conversion)
template <>
std::string value_to_string< std::string >(std::string const & str)
{
    return str;
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
// string -> string conversion (or no conversion)
template <>
std::string string_to_value< std::string >(std::string const & str)
{
    return str;
}

//----------------------------------------------------------------------
// string -> Float32_3 conversion
template <>
Float32_3 string_to_value< Float32_3 >(std::string const & val_str)
{
    Float32_3 const ret = string_to_vector_value< Float32, 3 >(val_str);
    return ret;
}

//----------------------------------------------------------------------
} // namespace dictionary_conv


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
// copy constructor
Dictionary::Dictionary(Dictionary const & rhs)
{
    m_dict_impl = rhs.m_dict_impl;
}

//----------------------------------------------------------------------
// operator=
Dictionary const & Dictionary::operator=(Dictionary const & rhs)
{
    if(this != &rhs){
        m_dict_impl = rhs.m_dict_impl;
    }
    return *this;
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
std::pair< Dictionary::iterator, bool >
Dictionary::insert(std::string const & key, Dictionary_value const & val)
{
    std::pair< Dictionary_map::iterator, bool > ret =
        m_dict_impl.insert(std::make_pair(key, val));
    if(!(ret.second)){
        // the key has been there, replace the value with the new one.
        (ret.first)->second = val;
    }
    return ret;
}

//----------------------------------------------------------------------
// insert all entries
Sint32 Dictionary::insert_all(Dictionary const & dict)
{
    Sint32 inserted_count = 0;
    for(const_iterator di = dict.begin(); di != dict.end(); ++di){
        std::pair< iterator, bool > ii = this->insert(di->first, di->second);
        if(ii.second){
            ++inserted_count;
        }
    }
    return inserted_count;
}

//----------------------------------------------------------------------
// erase an ently by its key
bool Dictionary::erase(std::string const & key)
{
    const_iterator di = m_dict_impl.find(key);
    if(di != m_dict_impl.end()){
        m_dict_impl.erase(key);
        return true;
    }
    // no entry
    return false;
}

//----------------------------------------------------------------------
// empty
bool Dictionary::empty() const
{
    return m_dict_impl.empty();
}

//----------------------------------------------------------------------
// size of dictionary
size_t Dictionary::size() const
{
    return m_dict_impl.size();
}

//----------------------------------------------------------------------
// const_iterator begin()
Dictionary::const_iterator Dictionary::begin() const
{
    return m_dict_impl.begin();
}

//----------------------------------------------------------------------
// const_iterator end()
Dictionary::const_iterator Dictionary::end() const
{
    return m_dict_impl.end();
}

//----------------------------------------------------------------------
// output parameters to stream, format: <line_prefix><key> = <value>
void Dictionary::write(std::ostream &os,
                       std::string const & prefix) const
{
    // if(is_sort){
    //     std::vector< std::string > sorted_line_buf; // including prefix
    //     for(Dictionary_map::const_iterator vi = m_dict_impl.begin();
    //         vi != m_dict_impl.end(); ++vi)
    //     {
    //         sorted_line_buf.push_back(
    //             prefix + vi->first + " = " + vi->second.get_string());
    //     }
    //     std::sort(sorted_line_buf.begin(), sorted_line_buf.end());
    //     for(std::vector< std::string >::const_iterator ki = sorted_line_buf.begin();
    //         ki != sorted_line_buf.end(); ++ki)
    //     {
    //         os << (*ki) << "\n";
    //     }
    // }
    // else{}
    for(Dictionary_map::const_iterator vi = m_dict_impl.begin();
        vi != m_dict_impl.end(); ++vi)
    {
        os << prefix << vi->first << " = " << vi->second.get_string() << "\n";
    }
}

//----------------------------------------------------------------------
// read dictionary from a stream
// void Dictionary::read(std::istream & is, std::string const & prefix);

//----------------------------------------------------------------------
// is all keys are defined in the dictionary?
bool is_all_key_defined(Dictionary const & dict,
                        std::vector< std::string > const & keyvec,
                        std::vector< std::string > * p_non_def_key_vec)
{
    std::vector< std::string > nondefvec;
    bool is_ok = true;
    const size_t keyvec_len = keyvec.size();
    for(size_t i = 0; i < keyvec_len; ++i){
        if(!(dict.is_defined(keyvec[i]))){
            is_ok = false;
            nondefvec.push_back(keyvec[i]);
        }
    }
    if(p_non_def_key_vec != 0){
        (*p_non_def_key_vec) = nondefvec;
    }
    return is_ok;
}

//----------------------------------------------------------------------
// is all keys are defined in the dictionary? This calls overloaded
bool is_all_key_defined(Dictionary const & dict,
                        char const * p_keyarray[],
                        std::vector< std::string > * p_non_def_key_vec)
{
    std::vector< std::string > keyvec;
    for(int i = 0; p_keyarray[i] != 0; i++){
        keyvec.push_back(std::string(p_keyarray[i]));
    }

    return is_all_key_defined(dict, keyvec, p_non_def_key_vec);
}

//----------------------------------------------------------------------
} // namespace ifgi

