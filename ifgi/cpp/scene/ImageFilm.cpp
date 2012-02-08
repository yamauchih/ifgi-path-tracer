//----------------------------------------------------------------------
// ifgi c++ implementation: ImageFilm.hh
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief scene element image film (frame buffer)

#include "ImageFilm.hh"
#include <cpp/base/LoadSavePPM.hh>
#include <cpp/base/GfiIO.hh>

namespace ifgi
{
//----------------------------------------------------------------------
// constructor.
ImageFilm::ImageFilm(Sint32_3 const & res, std::string const & buffername)
    :
    m_buffername(buffername),
    m_framebuffer(res[0], res[1], res[2])
{
    assert(res[0] > 0);
    assert(res[1] > 0);
    assert(res[2] > 0);
    // allocate buffer
    // m_framebuffer.resizeBuffer(res[0], res[1], res[2]);
}

//----------------------------------------------------------------------
// copy constructor
ImageFilm::ImageFilm(ImageFilm const & rhs)
{
    m_buffername  = rhs.m_buffername;
    m_framebuffer = rhs.m_framebuffer;
}

//----------------------------------------------------------------------
// operator=
ImageFilm const & ImageFilm::operator=(ImageFilm const & rhs)
{
    if(this != &rhs){
        m_buffername  = rhs.m_buffername;
        m_framebuffer = rhs.m_framebuffer;
    }
    return *this;
}

//----------------------------------------------------------------------
// get a color at pixel pos. This only works Zsize = 4 (RGBA)
Color ImageFilm::get_color(Sint32 x, Sint32 y) const
{
    assert(m_framebuffer.getZSize() == 4); // RGBA only
    Color const col(m_framebuffer.get(x, y, 0),
                    m_framebuffer.get(x, y, 1),
                    m_framebuffer.get(x, y, 2),
                    m_framebuffer.get(x, y, 3));
    return col;
}

//----------------------------------------------------------------------
// put a color at pixel (x,y).
void ImageFilm::put_color(Sint32 x, Sint32 y, Color const & col)
{
    assert(m_framebuffer.getDimension()[2] == 4); // RGBA assumed

    m_framebuffer.set(x, y, 0, col[0]);
    m_framebuffer.set(x, y, 1, col[1]);
    m_framebuffer.set(x, y, 2, col[2]);
    m_framebuffer.set(x, y, 3, col[3]);
}

//----------------------------------------------------------------------
// Fill the framebuffer with col.
void ImageFilm::fill_color(Color const & col)
{
    Sint32_3 const dim = m_framebuffer.getDimension();
    for(int x = 0; x < dim[0]; ++x){
        for(int y = 0; y < dim[1]; ++y){
            this->put_color(x, y, col);
        }
    }
}

//----------------------------------------------------------------------
// save the buffer contents to a file.
bool ImageFilm::save_file(std::string const & filename,
                          std::string const & filetype)
{
    Sint32_3 imgsize = m_framebuffer.getDimension();
    std::cout << "DEBUG: save_file: imgsize = " << imgsize << std::endl;
        
    if(filetype == "ppm"){
        bool const is_verbose = true;
        bool const ret = saveArray3DPPM(m_framebuffer, filename, is_verbose);
        return ret;
    }
    else if(filetype == "gfi"){
        bool const ret = save_gfi_to_array3d(m_framebuffer, filename);
        return ret;
    }
    throw Exception("Unknown filetype [" + filetype + "]");

    return false;
}

//----------------------------------------------------------------------
// get human readable string
std::string ImageFilm::to_string() const
{
    Sint32_3 const dim = m_framebuffer.getDimension();
    std::stringstream sstr;
    sstr << "[name: " << m_buffername << ", resolution: ("
         << dim[0] << " " << dim[1] << " " << dim[2] << ")]";
    return sstr.str();
}

//----------------------------------------------------------------------
} // namespace ifgi

