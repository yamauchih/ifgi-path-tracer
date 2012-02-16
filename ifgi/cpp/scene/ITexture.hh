//----------------------------------------------------------------------
// ifgi c++ implementation: ITexture.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief texture interface
#ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_ITEXTURE_HH
#define IFGI_PATH_TRACER_IFGI_CPP_SCENE_ITEXTURE_HH

#include <string>

#include <cpp/base/Vector.hh>

namespace ifgi
{

/// Texture interface
class ITexture
{
public:
    /// default constructor
    ITexture()
    {
        // empty
    }

    /// get class name.
    virtual std::string get_classname() const = 0;

    /// texture value.
    ///
    /// \param[in] _uv    texture uv coordinate (if surface)
    /// \param[in] _point texture point in 3d (if solid)
    /// \return texture color value
    /// FIXME may return const &.
    virtual Color value(// _uv, _point
        ) const = 0;
};

// class ImageTexture(object){
//     /// Image texture class///

//     def __init__(){
//         /// default constructor///
//         pass


//     def get_classname(){
//         /// get class name. interface method. (public).
//         \return class name
//         ///
//         assert 0, "get_classname must be implemented in a derived class."
//         return None


//     def value(_uv, _point){
//         /// texture value.

//         \param[in] _uv    texture uv coordinate (if surface);
//         \param[in] _point texture point in 3d (if solid);
//         \return texture color value
//         ///
//         assert 0, "value must be implemented in a derived class."
//         return None

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_ITEXTURE_HH
