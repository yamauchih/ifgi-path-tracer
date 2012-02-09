//----------------------------------------------------------------------
// ifgi c++ implementation: GfiIO.cpp
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief Matthias's gfi file IO with Array3D

#include "GfiIO.hh"

#include <cpp/extern/libnecro/gfi.h>
#include "Exception.hh"
#include "ILog.hh"

#include <cassert>
#include <fstream>

namespace ifgi {

//--------------------------------------------------------------------------------
// load gfi
bool load_gfi_to_array3d(std::string const & loadfname,
                         Array3D_Float32 &   a3d)
{
    std::cerr << "NIN load_gfi_to_array3d" << std::endl;
    // gfi_image_header header;
    // gfi_error_code code = gfi_read_image_header(&header, bmf->fp);
    // if (code != GFI_SUCCESS)
    // {
    //  logError("bitmap: %s %s", gfi_get_error_str(code), bmf->filename);
    //  return false;
    // }

    // if (header.num_channels != 3 && header.num_channels != 1)
    // {
    //  logError(
    //       "bitmap: wrong number of channels (%u) for file %s, expected 3 or 1",
    //       header.num_channels, bmf->filename);
    //  return false;
    // }

    // bm->type = BITMAP_TYPE_RGB_FLOAT;
    // bm->resX = header.res_x;
    // bm->resY = header.res_y;


    // const unsigned int n = bm->resX * bm->resY;
    // bm->data = bitmapcb.allocate(n * sizeof(float) * 3);
    // code = gfi_read_image_pixels(&header, (float *)bm->data, 0, bmf->fp);
    // if (code != GFI_SUCCESS)
    // {
    //  logError("bitmap: %s %s", gfi_get_error_str(code), bmf->filename);
    //  return false;
    // }

    // if (header.num_channels == 1)
    // {
    //  logVerbose("bitmap: converting gray-scale .gfi to rgb");
    //  float *p = (float *)bm->data;
    //  for (int i = int(bm->resX * bm->resY - 1); i >= 0; --i)
    //       p[3 * i] = p[i];

    //  for (unsigned int i = 0; i < bm->resX * bm->resY; ++i)
    //       p[3 * i + 2] = p[3 * i + 1] = p[3 * i];
    // }

    // return true;
    return false;
}

//--------------------------------------------------------------------------------
// save gfi
bool save_gfi_to_array3d(Array3D_Float32 const & a3d,
                         std::string const & savefname)
{
    Sint32_3 const imgdim = a3d.getDimension();

    // create a buffer for gfi
    gfi_image_header header;
    gfi_init_image_header(&header, "lightgrinder");
    header.res_x = imgdim[0];
    header.res_y = imgdim[1];
    header.num_channels = imgdim[2];

    FILE * pfp = fopen(savefname.c_str(), "w");
    if(pfp == 0){
        ILog::instance()->error("cannot open gfi file [" + savefname + "] for write.");
        return false;
    }

    gfi_error_code code = gfi_write_image_header(&header, pfp);
    if(code != GFI_SUCCESS){
        std::stringstream sstr;
        sstr << "gfi: [" << savefname << "], error: " << gfi_get_error_str(code) << "\n";
        ILog::instance()->error(sstr.str());
        return false;
    }

    int const reverse_scanlines = 1; // reverse scan lines
    code = gfi_write_image_pixels(&header, 
                                  const_cast< Array3D_Float32& >(a3d).peekDataArray(),
                                  reverse_scanlines, pfp);
    if(code != GFI_SUCCESS){
        std::stringstream sstr;
        sstr << "gfi: [" << savefname << "], error: " << gfi_get_error_str(code) << "\n";
        ILog::instance()->error(sstr.str());
        return false;
    }
    return true;
}


// /**
//    read raw (binary) data from an input stream with unix read()
//    syscall. retry until read() return 0

//    Read binary data, taking into account some amount of stalling
//    (e.g. gzip).  This function will retry (and wait) until the read()
//    syscall return the EOF just after clean the stream status.

//    \arg _in  read from stream
//    \arg _buf output buffer
//    \arg _sz  number of bytes to read
//    \return true when success
// */
// bool
// readRaw(std::istream& _in, char* _buf, size_t _sz)
// {
//   _in.read(_buf, _sz);

//   int nr       = _in.gcount();
//   int lastread = nr;

//   if (nr<0){
//     // std::cerr << "#Info readRaw0: read = " << nr << "/" << _sz << std::endl;
//     return false;
//   }

//   // read until specified size or last read size is 0.
//   while((nr!=int(_sz)) && (lastread > 0)){
//     // std::cerr << "_in.good() works? _in.good() = " << _in.good() << std::endl; not works
//     ::usleep(100); // give scheduler a chance

//     _in.clear();
//     _in.read(_buf+nr,_sz-nr);
//     lastread=_in.gcount();
//     nr+=lastread;

//     // std::cerr << "#Info readRaw: read = " << lastread << " " << nr << "/" << _sz
//     // << ", good = " << _in.good() << ", eof = " << _in.eof()
//     // << ", fail = " << _in.fail()
//     // << std::endl;
//   }

//   return nr==int(_sz);
// }

// //--------------------------------------------------------------------------------

// static inline int getIdx(const int _x,     const int _y, const int _z,
// 			 const int _xsize, const int _ysize, const int _zsize){
//   const int revy = (_ysize - 1) - _y; // reversed
//   return(((_x + (_xsize * revy)) * _zsize) + _z);
// }

// //--------------------------------------------------------------------------------

// bool
// loadPPMArray3D(const std::string&          _loadfname,
// 	       Array3D< float >& _a3d,
// 	       const bool                  _isverbose){
//   const std::string eh = "Error!: loadPPMArray3D: [" + _loadfname + "]: ";

//   // open the file.
//   std::fstream in;
//   in.open(_loadfname.c_str(), std::fstream::in);
//   if(!(bool)in){
//     std::cerr << eh << "can not open [" << _loadfname << "]." << std::endl;
//     return(false);
//   }

//   // read header
//   const int NBUF = 2048;
//   char buf[NBUF];

//   //   int tokens,value;
//   //   bool endOfHeader;
//   //   enum { WIDTH, HEIGHT, CDEPTH, EOH } status;

//   // first line should contain some signature P4, P5, or P6.
//   // in().getline(buf, NBUF);
//   in.getline(buf, NBUF);
//   const std::string magic(buf);
//   if((magic != "P5") && (magic != "P6")){
//     std::cerr << eh << "can not read. this only treats P5 or P6 format." << std::endl;
//     return(false);
//   }

//   // parse header
//   while(!(in.eof())){
//     in.getline(buf, NBUF);
//     if(buf[0] == '#'){		// skip comment
//       continue;
//     }
//     else{
//       break;			// end of comment
//     }
//   }

//   // get the size
//   int xsize = -1, ysize = -1;
//   if((sscanf(buf, "%d %d", &xsize, &ysize) != 2)){
//     std::cerr << eh << "unrecognized header (size). buf:" << buf << std::endl;
//     return(false);
//   }
//   // get the depth
//   int depth = -1;
//   if((bool)in && (in.getline(buf, NBUF))){
//     if((sscanf(buf, "%d", &depth) != 1)){
//       std::cerr << eh << "unrecognized header (depth). buf:" << buf << std::endl;
//       return(false);
//     }
//   }
//   else{
//     std::cerr << eh << "unexpected eof." << std::endl;
//     return(false);
//   }

//   if((xsize <= 0) || (ysize <= 0) || (depth != 255)){
//     std::cerr << eh << "illegal parameter. xsize, ysize, depth = "
// 	      << xsize << ", " << ysize << ", " << depth << std::endl;
//     return(false);
//   }

//   // read image
//   const int zsize = (magic == "P5") ? 1 : 3;

//   if(_isverbose){
//     std::cerr << "[Verbose]: [" << _loadfname << "] xsize, ysize, channels, depth = "
// 	      << xsize << ", " << ysize << ", " << zsize << ", " << depth << std::endl;
//   }

//   const int IMGBUFSIZE = xsize * ysize * zsize;
//   char* pImgBuf        = new char[IMGBUFSIZE];
//   {
//     // in().read(pImgBuf, IMGBUFSIZE);
//     bool r = readRaw(in, pImgBuf, IMGBUFSIZE);
//     if(!r){
//       std::cerr << eh << "read fail." << std::endl;
//       return(false);
//     }

//     _a3d.resizeBuffer(xsize, ysize, zsize);
//     for(int x = 0; x < xsize; x++){
//       for(int y = 0; y < ysize; y++){
// 	for(int z = 0; z < zsize; z++){
// 	  const int idx = getIdx(x, y, z, xsize, ysize, zsize);
// 	  assert((0 <= idx) && (idx < IMGBUFSIZE));
// 	  const float val = ((float)((unsigned char)(pImgBuf[idx]))) / 255.0;
// 	  _a3d.set(x, y, z, val);
// 	  // std::cout << "DEBUG:[" << x << "," << y << "," << z << "]=" << val << std::endl;
// 	}
//       }
//     }
//   }
//   delete pImgBuf;
//   pImgBuf = 0;

//   // std::cerr << "DEBUG: eof = " << in().eof() << ", fail = " << in().fail() << std::endl;

//   if(!(bool)in){
//     std::cerr << eh << "illegal file size (truncated?)." << std::endl;
//     return(false);
//   }

//   return(true);
// }

// //--------------------------------------------------------------------------------

// bool
// saveArray3DPPM(const Array3D< float >& _a3d,
// 	       const std::string&                _savefname,
// 	       const bool                        _isverbose){
//   const std::string eh = "Error!: saveArray3DPPM: [" + _savefname + "]: ";

//   // open the file.
//   std::fstream out;
//   out.open(_savefname.c_str(), std::fstream::out);
//   if(!out.good()){
//     std::cerr << eh << "can not open [" << _savefname << "]." << std::endl;
//     return(false);
//   }

//   // write the header
//   const int xsize = _a3d.getXSize();
//   const int ysize = _a3d.getYSize();
//   int       zsize = _a3d.getZSize();

//   if(zsize == 1){
//     out << "P5" << std::endl;
//   }
//   else if (zsize == 3){
//     out << "P6" << std::endl;
//   }
//   else if (zsize == 4){
//     out << "P6" << std::endl;
//     std::cerr << "Warn: zsize == 4, ignored alpha channel." << std::endl;
//     zsize = 3;                  // changed
//   }
//   else{
//       std::cerr << eh << "can not save PPM from ZSize == " << zsize << std::endl;
//       return false;
//   }

//   if(_isverbose){
//     std::cerr << "[Verbose]: [" << _savefname << "] xsize, ysize, channels = "
// 	      << xsize << ", " << ysize << ", " << zsize << std::endl;
//   }

//   Date now;
//   out << "# created by saveArray3DPPM. " << now.toCTimeStr() << std::endl;
//   out << xsize << " " << ysize << std::endl;
//   out << "255" << std::endl;

//   // save buffer
//   const int IMGBUFSIZE   = xsize * ysize * zsize;
//   unsigned char* pImgBuf = new unsigned char[IMGBUFSIZE];
//   {
//     for(int x = 0; x < xsize; x++){
//       for(int y = 0; y < ysize; y++){
// 	for(int z = 0; z < zsize; z++){
// 	  const int idx = getIdx(x, y, z, xsize, ysize, zsize);
// 	  assert((0 <= idx) && (idx < IMGBUFSIZE));
// 	  const unsigned char val = (unsigned char)(255.0 * _a3d.get(x, y, z));
// 	  pImgBuf[idx] = val;
// 	}
//       }
//     }
//     out.write((char *)pImgBuf, IMGBUFSIZE);
//   }
//   delete pImgBuf;
//   pImgBuf = 0;

//   bool r = (bool)out;
//   if(!r){
//     std::cerr << eh << "write failed. File system is full?" << std::endl;
//   }
//   out.close();
//   return(r);
// }

//--------------------------------------------------------------------------------
} // namespace imgsynth
