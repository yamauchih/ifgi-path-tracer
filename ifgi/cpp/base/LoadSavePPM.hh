//----------------------------------------------------------------------
// ifgi c++ implementation: LoadSavePPM.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief LoadSavePPM.hh based on imgsynth LoadSavePPM.hh

#ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_LOADSAVEPPM_HH
#define IFGI_PATH_TRACER_IFGI_CPP_BASE_LOADSAVEPPM_HH

#include "Array3D.hh"
#include <string>

namespace ifgi
{

//--------------------------------------------------------------------------------
/**
   load PPM file.

   \param _loadfname filename to load.

   \param _a3d       (output) the image
   \param _isverbose when true, set the verbose mode.
   \return true when the load is succeeded.
*/
extern bool
loadPPMArray3D(const std::string&          _loadfname,
	       Array3D< float >& _a3d,
	       const bool                  _isverbose = false);

//--------------------------------------------------------------------------------
/**
   save PPM file.

   \param _a3d       the image to save.
   \param _savefname save filename
   \param _isverbose when true, set the verbose mode.
   \return true when the save is succeeded.
*/
extern bool
saveArray3DPPM(const Array3D< float >& _a3d,
	       const std::string&                _savefname,
	       const bool                        _isverbose = false);

//--------------------------------------------------------------------------------
} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_LOADSAVEPPM_HH
