//----------------------------------------------------------------------
// ifgi c++ implementation: GfiIO.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief Matthias's gfi file IO with Array3D

#ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_GFIIO_HH
#define IFGI_PATH_TRACER_IFGI_CPP_BASE_GFIIO_HH

#include "Array3D.hh"
#include <string>

namespace ifgi
{
//--------------------------------------------------------------------------------
/// load gfi
///
/// \param[in]  fname filename to load.
/// \param[out] a3d   (output) the image array for load
/// \return true when the load is succeeded.
extern bool
load_gfi_to_array3d(std::string const & loadfname,
                    Array3D_Float32 &   a3d);

//--------------------------------------------------------------------------------
/// save gfi
///
/// \param[in]  a3d   the image array to be saved
/// \param[in]  savefname filename to save.
/// \return true when the save is succeeded.
extern bool
save_gfi_to_array3d(Array3D_Float32 const & a3d,
                    std::string const & savefname);

//--------------------------------------------------------------------------------
} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_GFIIO_HH
