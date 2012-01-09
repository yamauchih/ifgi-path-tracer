//----------------------------------------------------------------------
// ifgi c++ implementation: ConstantColorTexture.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief constant color texture
#ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_CONSTANTCOLORTEXTURE_HH
#define IFGI_PATH_TRACER_IFGI_CPP_SCENE_CONSTANTCOLORTEXTURE_HH

#include "ITexture.hh"

namespace ifgi {

/// Constant color texture
class ConstantColorTexture : public ITexture
{
public:
    /// default constructor
    ///
    /// \param[in] col constant color
    ConstantColorTexture(Color const & col);

    /// destructor
    virtual ~ConstantColorTexture();

    /// set constant color.
    /// \param[in] col constant color of this texture
    void set_constant_color(Color const & col);

public:
    /// get class name. interface method. (public).
    /// \return class name
    virtual std::string get_classname() const ;

    /// texture value.
    ///
    /// \param[in] uv    texture uv coordinate (if surface);
    /// \param[in] point texture point in 3d (if solid);
    /// \return texture color value
    virtual Color value(// _uv, point){
        ) const;

private:
    /// constant texture color
    Color m_color;

private:
    /// copy constructor, never used.
    ConstantColorTexture(ConstantColorTexture const & rhs);
    /// operator=, never used.
    ConstantColorTexture const & operator=(ConstantColorTexture const & rhs);
};

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_CONSTANTCOLORTEXTURE_HH
