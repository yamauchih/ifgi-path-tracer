//----------------------------------------------------------------------
// ifgi c++ implementation: Film.hh
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief scene element film (A camera has this.)
#ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_FILM_HH
#define IFGI_PATH_TRACER_IFGI_CPP_SCENE_FILM_HH
namespace ifgi
{
// from PIL import Image
// import numpy

/// TODO: maybe reuse imgsynth's array2d or something check it out!


/// image film (frame buffer)
///
/// PIXEL_T = { Color, Float32 }. Color ... RGBA buffer, Float32 ... ex. Z



template < typename PIXEL_T >
class ImageFilm
{
public:
    /// constructor.
    /// \param[in] res  resolution (x, y) resolution.
    /// \param[in] buffername buffer name (RGBA, Z, ...);
    ImageFilm(Sint32_3 const & res, std::string const & buffername)
    {
        m_resolution = res
        assert(m_resolution[0] > 0);
        assert(m_resolution[1] > 0);

        m_buffername = buffername

        /// allocate buffer: zeros((shepe_touple), type, ...);
        m_framebuffer = numpy.zeros((m_resolution[0],
                                          m_resolution[1],
                                     m_resolution[2]));
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
        return m_resolution;
    }

    /// get a color at pixel pos.
    ///
    /// \param[in] pos position of the pixel (x,y)
    /// \return a color of pos(x,y)
    Color const & get_color(Sint32_2 const & pos) const
    {
        return m_framebuffer[_pos];
    }

    /// put a color at pixel pos.
    ///
    /// \param[in] pos   position as pixel (tuple), e.g., (80, 120);
    /// \param[in] color pixel color as numpy.array. e.g., [1.0, 0.0, 0.0, 1.0]
    void put_color(Sint32_2 const & pos, Color const & color)
    {
        assert(((len(_pos) == 2) && (len(_color) == m_resolution[2])) or
               ((len(_pos) == 3) && (len(_color) == 1)));
        m_framebuffer[_pos] = color;
    }

    /// Fill the framebuffer with col.
    ///
    /// \param[in] col color to be filled
    void fill_color(Color const & col)
    {
        for(x in xrange(0, m_resolution[0], 1)){
            for(y in xrange(0, m_resolution[1], 1)){
                m_framebuffer[(x, y)] = col;
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
    /// buffer resolution
    Sint32_2 m_resolution;
    /// buffer name
    std::string m_buffername;
};

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_FILM_HH
