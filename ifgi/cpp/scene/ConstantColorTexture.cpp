//----------------------------------------------------------------------
// ifgi c++ implementation: ConstantColorTexture.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief constant color texture

#include "ConstantColorTexture.hh"

namespace ifgi {

//----------------------------------------------------------------------
// default constructor
ConstantColorTexture::ConstantColorTexture(Color const & col)
    :
    m_color(col)
{
    // empty
}

//----------------------------------------------------------------------
// destructor
ConstantColorTexture::~ConstantColorTexture()
{
    // empty
}

//----------------------------------------------------------------------
// set constant color.
void ConstantColorTexture::set_constant_color(Color const & col)
{
    m_color = col;
}

//----------------------------------------------------------------------
// get class name. interface method. (public).
std::string ConstantColorTexture::get_classname() const
{
    return "ConstantColorTexture";
}

//----------------------------------------------------------------------
// texture value.
Color ConstantColorTexture::value(// _uv, point){
    ) const
{
    return m_color;
}

//----------------------------------------------------------------------
} // namespace ifgi

