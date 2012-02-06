//----------------------------------------------------------------------
// ifgi c++ implementation: OrthonomalBasis.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief OrthonomalBasis
//
// Ref. Realistic Ray Tracing by Peter Shirley
//
#ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_ORTHONOMALBASIS_HH
#define IFGI_PATH_TRACER_IFGI_CPP_BASE_ORTHONOMALBASIS_HH

#include <sstream>

#include "types.hh"
#include "Vector.hh"

namespace ifgi
{
/// OrthonomalBasis
class OrthonomalBasis
{
public:
    /// orthonomal basis epsilon
    static const  Scalar ONB_EPSILON = 0.001;
    /// standard basis 0
    /// can not do for non POD, we can only declare the static const member.
    /// static const Scalar_3 Vec3_N;(1.0, 0.0, 0.0);
    static const Scalar_3 Vec3_N;
    /// standard basis 1
    static const Scalar_3 Vec3_M;


    /// default constructor
    OrthonomalBasis()
        :
        m_U(Vec3_N),
        m_V(Vec3_M),
        m_W(Scalar(0.0), Scalar(0.0), Scalar(1.0))
    {
        // empty
    }

    /// set all the component of orthonomal basis.
    /// \param[in] u u component
    /// \param[in] v v component
    /// \param[in] w w component
    void set(Scalar_3 const & u, 
             Scalar_3 const & v, 
             Scalar_3 const & w)
    {
        m_U = u;
        m_V = v;
        m_W = w;
    }

    /// get u component.
    /// \return u component.
    Scalar_3 const & u() const 
    {
        return m_U;
    }

    /// get v component.
    /// \return v component.
    Scalar_3 const & v() const
    {
        return m_V;
    }

    /// get w component.
    /// \return w component./// 
    Scalar_3 const & w() const
    {
        return m_W;
    }

    /// normali the vector
    /// \param[in] vec input vector to normalize.
    /// length should be > ONB_EPSILON
    // void normalize(Scalar_3 & vec)
    // {
    //     len = numpy.linalg.norm(_vec);
    //     assert(len > OrthonomalBasis.ONB_EPSILON);
    //     return vec / len;
    // }
    // DELETEME
            
    /// initialize from u component.
    /// \param[in] u u component.
    void init_from_u(Scalar_3 const & u)
    {
        m_U = u;
        m_U.normalize();
        m_V = cross(m_U, OrthonomalBasis::Vec3_N);
        Scalar const v_len = m_V.norm();
        if(v_len < OrthonomalBasis::ONB_EPSILON){
            m_V = cross(m_U, OrthonomalBasis::Vec3_M);
        }
        m_W = cross(m_U, m_V);
    }

    /// initialize from v component.
    /// \param[in] v v component.
    void init_from_v(Scalar_3 const & v)
    {
        m_V = v;
        m_V.normalize();
        m_U = cross(m_V, OrthonomalBasis::Vec3_N);
        Scalar const u_len = m_U.norm(); // FIXME sqrnorm
        if(u_len < OrthonomalBasis::ONB_EPSILON){
            m_U = cross(m_V, OrthonomalBasis::Vec3_M);
        }
        m_W = cross(m_U, m_V);
    }

    /// initialize from w component.
    /// \param[in] w w component.
    void init_from_w(Scalar_3 const & w)
    {
        m_W = w;
        m_W.normalize();
        m_U = cross(m_W, OrthonomalBasis::Vec3_N);
        Scalar const u_len = m_U.norm();
        if(u_len < OrthonomalBasis::ONB_EPSILON){
            m_U = cross(m_W, OrthonomalBasis::Vec3_M);
        }
        m_V = cross(m_W, m_U);
    }

    /// initialize from uv component.
    /// \param[in] u u component.
    /// \param[in] v v component.
    void init_from_uv(Scalar_3 const & u, Scalar_3 const & v)
    {
        m_U = u;
        m_U.normalize();
        m_W = cross(u, v).normalize();
        m_V = cross(m_W, m_U);
    }
        
    /// initialize from vw component.
    /// \param[in] v v component.
    /// \param[in] w w component.
    void init_from_vw(Scalar_3 const & v, 
                      Scalar_3 const & w)
    {
        m_V = v;
        m_V.normalize();
        m_U = cross(v, w).normalize();
        m_W = cross(m_U, m_V);
    }

    /// initialize from wu component.
    /// \param[in] w w component.
    /// \param[in] u u component.
    void init_from_wu(Scalar_3 const & w, 
                      Scalar_3 const & u)
    {
        m_W = w;
        m_W.normalize();
        m_V = cross(w, u).normalize();
        m_U = cross(m_V, m_W);
    }

    /// get human readable string
    /// \return string representation
    std::string to_string() const
    {
        std::stringstream sstr;
        sstr << "[" << this->u()[0] << " " << this->u()[1] << " " << this->u()[2] << "] "
             << "[" << this->v()[0] << " " << this->v()[1] << " " << this->v()[2] << "] "
             << "[" << this->w()[0] << " " << this->w()[1] << " " << this->w()[2] << "] ";
        return sstr.str();
    }
private:
    /// orthogonal basis U
    Scalar_3 m_U;
    /// orthogonal basis V
    Scalar_3 m_V;
    /// orthogonal basis W
    Scalar_3 m_W;
};

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_ORTHONOMALBASIS_HH
