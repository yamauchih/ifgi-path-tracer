//----------------------------------------------------------------------
// ifgi c++ implementation: ImageFilm.hh
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief scene element image film (frame buffer)
#ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_IMAGEFILM_HH
#define IFGI_PATH_TRACER_IFGI_CPP_SCENE_IMAGEFILM_HH

#include <cpp/base/Array3D.hh>

namespace ifgi
{

/// image film (frame buffer)
class ImageFilm
{
public:
    /// constructor.
    /// \param[in] res  resolution (x, y) resolution.
    /// \param[in] buffername buffer name (RGBA, Z, ...);
    ImageFilm(Sint32_3 const & res, std::string const & buffername);

    /// copy constructor
    ImageFilm(ImageFilm const & rhs);

    /// operator=
    ImageFilm const & operator=(ImageFilm const & rhs);

    /// get class name.
    /// \return class name
    std::string get_classname() const
    {
        return std::string("ImageFilm");
    }

    /// get buffer name (buffer instance name).
    /// \return buffer name
    std::string get_buffername() const
    {
        return m_buffername;
    }

    /// get the film resolution.
    ///
    /// \return resolution, e.g., (1024, 800, 3) = image size
    /// 1024x800, 3 channels.
    Sint32_3 get_resolution() const
    {
        return m_framebuffer.getDimension();
    }

    /// get a value
    ///
    /// \param[in] aidx array index (x,y,z)
    /// \return a value of (x,y,z)
    Scalar const get_value(Sint32_3 const & aidx) const
    {
        return m_framebuffer.get(aidx[0], aidx[1], aidx[2]);
    }

    /// set a value
    ///
    /// \param[in] aidx array index (x,y,z)
    /// \param[in] val  value to set
    void set_value(Sint32_3 const & aidx, Scalar val)
    {
        m_framebuffer.set(aidx[0], aidx[1], aidx[2], val);
    }

    /// get a color at pixel pos. This only works Zsize = 4 (RGBA)
    ///
    /// \param[in] x x index
    /// \param[in] y y index
    /// \return a color of pos(x,y)
    Color get_color(Sint32 x, Sint32 y) const;

    /// put a color at pixel (x,y).
    ///
    /// \param[in] x x index
    /// \param[in] y y index
    /// \param[in] col a color of pos(x,y)
    void put_color(Sint32 x, Sint32 y, Color const & col);

    /// Fill the framebuffer with col.
    ///
    /// \param[in] col color to be filled
    void fill_color(Color const & col);

    /// save the buffer contents to a file.
    /// \param[in] filename output file name
    /// \param[in] filetype output file type. {"ppm","gfi"}
    /// \return true when succeeded
    bool save_file(std::string const & filename, std::string const & file_type);

    /// get human readable string
    /// \return string representation of this object
    std::string to_string() const;

private:
    /// buffer name
    std::string m_buffername;
    /// the buffer
    Array3D_Float32 m_framebuffer;
};

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_IMAGEFILM_HH
