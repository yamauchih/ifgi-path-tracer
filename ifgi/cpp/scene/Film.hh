//----------------------------------------------------------------------
// ifgi c++ implementation: Film.hh
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief scene element film (A camera has this.)
#ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_FILM_HH
#define IFGI_PATH_TRACER_IFGI_CPP_SCENE_FILM_HH

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
    ImageFilm(Sint32_3 const & res, std::string const & buffername)
        :
        m_buffername(buffername),
        m_framebuffer(res[0], res[1], res[2]);
    {
        assert(res[0] > 0);
        assert(res[1] > 0);
        assert(res[2] > 0);
        // allocate buffer
        // m_framebuffer.resizeBuffer(res[0], res[1], res[2]);
    }

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
    Sint32_3 const & get_resolution() const
    {
        return m_framebuffer.getDimension();
    }

    /// get a value
    ///
    /// \param[in] aidx array index (x,y,z)
    /// \return a value of (x,y,z)
    Float32 const get_value(Sint32_3 const & aidx) const
    {
        return m_framebuffer.get(aidx[0], aidx[1], aidx[2]);
    }

    /// set a value
    ///
    /// \param[in] aidx array index (x,y,z)
    /// \param[in] val  value to set
    void set_value(Sint32_3 const & aidx, Float32 val) const
    {
        m_framebuffer.set(aidx[0], aidx[1], aidx[2], val);
    }

    /// get a color at pixel pos. This only works Zsize = 4 (RGBA)
    ///
    /// \param[in] x x index
    /// \param[in] y y index
    /// \return a color of pos(x,y)
    Color const & get_color(Sint32 x, Sint32 y) const
    {
        assert(m_framebuffer.getZSize() == 4); // RGBA only
        Color const col(m_framebuffer.get(x, y, 0),
                        m_framebuffer.get(x, y, 1),
                        m_framebuffer.get(x, y, 2),
                        m_framebuffer.get(x, y, 3));
        return col;
    }

    /// put a color at pixel (x,y).
    ///
    /// \param[in] x x index
    /// \param[in] y y index
    /// \param[in] col a color of pos(x,y)
    void put_color(Sint32 x, Sint32 y, Color const & col)
    {
        m_framebuffer.set(x, y, 0, col[0]);
        m_framebuffer.set(x, y, 1, col[1]);
        m_framebuffer.set(x, y, 2, col[2]);
        m_framebuffer.set(x, y, 3, col[3]);
    }

    /// Fill the framebuffer with col.
    ///
    /// \param[in] col color to be filled
    void fill_color(Color const & col)
    {
        Sint32_3 const dim = m_framebuffer.getDimension();
        for(int x = 0; x < dim[0], ++x){
            for(int y = 0; y < dim[1], ++y){
                this->put_color(x, y, col);
            }
        }
    }

    /// save the buffer contents to a file.
    /// \param[in] filename output file name
    // bool save_file(std::string const filename)
    // {
    //     imgsize  = (m_resolution[0], m_resolution[1]);
    //     print imgsize

    //     if(m_resolution[2] == 1){
    //         /// grayscale -> convert to RGB
    //         bg_white = (255, 255, 255);
    //         img = Image.new("RGB", imgsize, bg_white);

    //         for x in xrange(0, m_resolution[0], 1){
    //             for y in xrange(0, m_resolution[1], 1){
    //                 col = this->get_color(_pos);
    //                 /// duplicate the channels
    //                 ucharcol = (255 * col[0], 255 * col[0], 255 * col[0]);
    //                 img.putpixel((x, m_resolution[1] - y - 1), ucharcol);
    //                 }
    //             }
    //     }
    //     elif(m_resolution[2] == 3){
    //         // RGB
    //         bg_white = (255, 255, 255);
    //         img = Image.new("RGB", imgsize, bg_white);

    //         for x in xrange(0, m_resolution[0], 1){
    //             for y in xrange(0, m_resolution[1], 1){
    //                 col = this->get_color(_pos);
    //                 ucharcol = (255 * col[0], 255 * col[1], 255 * col[2]);
    //                 img.putpixel((x, m_resolution[1] - y - 1), ucharcol);

    //     elif(m_resolution[2] == 4){
    //         /// RGBA
    //         bg_white = (255, 255, 255, 255);
    //         img = Image.new("RGBA", imgsize, bg_white);

    //         for x in xrange(0, m_resolution[0], 1){
    //             for y in xrange(0, m_resolution[1], 1){
    //                 col = 255 * this->get_color((x, y));
    //                 ucharcol = (int(col[0]), int(col[1]), int(col[2]), int(col[3]));
    //                 img.putpixel((x, m_resolution[1] - y - 1), ucharcol);
    //     else:
    //         raise StandardError, ("supported number of channels are 1, 3, && 4, only.");

    //     img.save(_filename);
    //                 }

    /// human readable string
    // def _str__(){

    //     return "[name: %s, resolution: (%d %d %d)]" \
    //         % (m_buffername,  m_resolution[0], \
    //                m_resolution[1], m_resolution[2]);
private:
    /// buffer name
    std::string m_buffername;
    /// the buffer
    Array3D_Float32 m_framebuffer;
};

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_FILM_HH
