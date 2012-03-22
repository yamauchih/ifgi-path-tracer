//----------------------------------------------------------------------
// RingBuffer.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief ring buffer

#include "RingBuffer.hh"

#include <sstream>
#include <iostream>

namespace ifgi
{
//----------------------------------------------------------------------
// default constructor. With default buffer size 1024.
RingBuffer::RingBuffer()
    :
    m_data_buf(),
    m_buf_size(0),
    m_begin_idx(0),
    m_end_idx(0),
    m_data_size(0)
{
    this->resize_buffer(1024);
}

//----------------------------------------------------------------------
// constructor
RingBuffer::RingBuffer(size_t buf_size)
    :
    m_data_buf(),
    m_buf_size(0),
    m_begin_idx(0),
    m_end_idx(0),
    m_data_size(0)
{
    this->resize_buffer(buf_size);
}

//----------------------------------------------------------------------
// destructor
RingBuffer::~RingBuffer()
{
    m_data_buf.clear();
    m_buf_size  = 0;
    m_begin_idx = 0;
    m_end_idx   = 0;
    m_data_size = 0;
}

//----------------------------------------------------------------------
// clear the buffer
void RingBuffer::clear()
{
    m_begin_idx = 0;
    m_end_idx   = 0;
    m_data_size = 0;
}

//----------------------------------------------------------------------
// set the buffer size. The data is lost.
void RingBuffer::resize_buffer(size_t buf_size)
{
    assert(buf_size > 0);

    m_data_buf.resize(buf_size);
    m_buf_size  = buf_size;
    m_begin_idx = 0;
    m_end_idx   = 0;
    m_data_size = 0;

    assert(m_buf_size == m_data_buf.size());
}

//----------------------------------------------------------------------
// push back a data at the end
void RingBuffer::push_back(value_type const & val)
{
    if(this->full()){
        // remove the begin and push back at the end
        // std::cout << "full" << std::endl;
        this->pop_front();
    }
    if(this->empty()){
        // if empty(), we just insert the data at the current end
        // position. No end move, but the size is increase.
        ++m_data_size;
        assert(m_end_idx < m_data_buf.size());
        m_data_buf[m_end_idx] = val;
    }
    else{
        this->inc_end();
        assert(m_end_idx < m_data_buf.size());
        m_data_buf[m_end_idx] = val;
    }
}

//----------------------------------------------------------------------
// pop front the data
void RingBuffer::pop_front()
{
    this->inc_begin();
}

//----------------------------------------------------------------------
// get front. access to the 0th data.
RingBuffer::value_type const & RingBuffer::front() const
{
    assert(!this->empty());
    assert(m_begin_idx < m_data_buf.size());

    return m_data_buf[m_begin_idx];
}

//----------------------------------------------------------------------
// get back. access to the n-1th data.
RingBuffer::value_type const & RingBuffer::back() const
{
    assert(!this->empty());
    assert(m_end_idx < m_data_buf.size());

    return m_data_buf[m_end_idx];
}

//----------------------------------------------------------------------
// get valid data size
size_t RingBuffer::size() const
{
    return m_data_size;
}

//----------------------------------------------------------------------
// get the capacity (buffer size)
size_t RingBuffer::capacity() const
{
    return m_buf_size;
}

//----------------------------------------------------------------------
// is empty the data?
bool RingBuffer::empty() const
{
    if(m_data_size == 0){
        assert(m_begin_idx == m_end_idx);
        return true;
    }
    assert(m_data_size > 0);
    return false;
}

//----------------------------------------------------------------------
// is full the buffer?
bool RingBuffer::full() const
{
    if(m_data_size == m_buf_size){
        return true;
    }
    return false;
}

//----------------------------------------------------------------------
// to string
std::string RingBuffer::to_string() const
{
    assert(m_data_buf.size() == m_buf_size);

    std::stringstream sstr;
    sstr << "buffsize: " << m_data_buf.size()
         << ", internal index [" << m_begin_idx << "," << m_end_idx
         << "], datasize: " << m_data_size;
    if(this->empty()){
        sstr << ", empty.";
    }
    if(this->full()){
        sstr << ", full.";
    }

    return sstr.str();
}

//----------------------------------------------------------------------
// iterator begin
RingBuffer::iterator RingBuffer::begin()
{
    return RingBuffer::iterator(this, true);
}

//----------------------------------------------------------------------
// iterator end
RingBuffer::iterator RingBuffer::end()
{
    return RingBuffer::iterator(this, false);
}

//----------------------------------------------------------------------
// increment the begin when not empty
void RingBuffer::inc_begin()
{
    assert(!this->empty());
    assert(m_data_size > 0);

    ++m_begin_idx;
    --m_data_size;

    // if index is over the buffer, back to 0
    if(m_begin_idx == m_buf_size){
        m_begin_idx = 0;
    }

    assert(m_begin_idx < m_buf_size);
}

//----------------------------------------------------------------------
// increment the end when not full
void RingBuffer::inc_end()
{
    assert(!this->full());

    ++m_end_idx;
    ++m_data_size;
    assert(m_data_size <= m_buf_size);

    // if index is over the buffer, back to 0
    if(m_end_idx == m_buf_size){
        m_end_idx = 0;
    }

    assert(m_end_idx < m_buf_size);
}

//----------------------------------------------------------------------
} // namespace ifgi
