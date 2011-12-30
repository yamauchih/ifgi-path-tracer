//----------------------------------------------------------------------
// ifgi c++ implementation: Vector.hh
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief N component vector and some specialization
#ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_VECTOR_HH
#define IFGI_PATH_TRACER_IFGI_CPP_BASE_VECTOR_HH

#include <cassert>
#include <cmath>
#include <cstring>
#include <iostream>


#include "types.hh"


namespace ifgi
{
//----------------------------------------------------------------------

// forward declaration for friends. 'friend' in the Vector template
// class needs declaration.
template< typename Scalar, int DIM > class Vector;
template< typename Scalar >
Vector<Scalar,3> cross(Vector<Scalar,3> const & v0,
                       Vector<Scalar,3> const & v1);

//----------------------------------------------------------------------

/// A vector is an array of size DIM of type Scalar
template< typename Scalar, int DIM >
class Vector {
public:
    /// the type of the scalar used in this template
    typedef Scalar value_type;
    /// returns size DIM of the vector
    static inline int dim() { return DIM; }

    /// default constructor
    /// creates uninitialized values.
    inline Vector()
    {
        // empty
    }

    /// constructor with 1 explicit value. only valid for 1 DIM
    /// \param[in] v0 first component of vector
    explicit inline Vector(Scalar const & v0)
    {
        assert(DIM == 1);
        m_value[0] = v0;
    }

    /// constructor with 2 explicit values. only valid for 2 DIM
    /// \param[in] v0 v0 component of vector
    /// \param[in] v1 v1 component of vector
    explicit inline Vector(Scalar const & v0, Scalar const & v1)
    {
        assert(DIM == 2);
        m_value[0] = v0;
        m_value[1] = v1;
    }

    /// constructr with 3 explicit values. only valid for 3 DIM
    /// \param[in] v0 v0 component of vector
    /// \param[in] v1 v1 component of vector
    /// \param[in] v2 v2 component of vector
    explicit inline Vector(Scalar const & v0, Scalar const & v1,
                           Scalar const & v2)
    {
        assert(DIM == 3);
        m_value[0] = v0;
        m_value[1] = v1;
        m_value[2] = v2;
    }

    /// constructr with 4 explicit values. only valid for 4 DIM
    /// \param[in] v0 v0 component of vector
    /// \param[in] v1 v1 component of vector
    /// \param[in] v2 v2 component of vector
    /// \param[in] v3 v3 component of vector
    explicit inline Vector(Scalar const & v0, Scalar const & v1,
                           Scalar const & v2, Scalar const & v3)
    {
        assert(DIM == 4);
        m_value[0] = v0;
        m_value[1] = v1;
        m_value[2] = v2;
        m_value[3] = v3;
    }

    /// Construct from a value array
    // explicit inline Vector(const Scalar value[DIM])
    // {
    //     memcpy(m_value, m_value, DIM * sizeof(Scalar));
    // }

    /// copy constructor (same kind of vector)
    /// \param[in] rhs right hand side
    inline Vector(Vector< Scalar, DIM > const &rhs)
    {
        this->operator=(rhs);
    }

    /// operator=
    /// \param[in] rhs right hand side
    inline Vector< Scalar, DIM > &operator=(Vector< Scalar, DIM > const & rhs)
    {
        if(&rhs != this){
            memcpy(m_value, rhs.m_value, DIM * sizeof(Scalar));
        }
        return *this;
    }

    /// get idx'th element read-write
    /// \param[in] idx right hand side
    inline Scalar & operator[](int idx)
    {
        assert((idx >= 0) && (idx < DIM));
        return m_value[idx];
    }

    /// get idx'th element read-only
    inline Scalar const & operator[](int idx) const
    {
        assert((idx >= 0) && (idx < DIM));
        return m_value[idx];
    }

    /// compose vector containing the same value in each component
    // static inline Vector< Scalar, DIM > vectorize(Scalar value) {
    //     Vector< Scalar, DIM > result;
    //     for(int i=0; i<N; i++)
    //         result[i] = value;
    //     return result;
    // }

    /// component-wise comparison
    inline bool operator==(Vector< Scalar, DIM> const & rhs) const
    {
        for(int i = 0; i < DIM; ++i){
            if(m_value[i] != rhs.m_value[i]){
                return false;
            }
        }
        return true;
    }

    /// component-wise comparison
    inline bool operator!=(Vector< Scalar, DIM > const & rhs) const
    {
        for(int i = 0; i < DIM; i++){
            if(m_value[i] != rhs.m_value[i]){
                return true;
            }
        }
        return false;
    }

    /// get norm of the vector
    /// \return norm of the vector
    inline Scalar norm() const
    {
        return((Scalar)sqrt((double)this->sqrnorm()));
    }

    /// get squared norm of the vector
    /// \return squared norm of the vector
    inline Scalar sqrnorm() const
    {
        return this->dot(*this);
    }

    /// compute maximum norm (absolute value), return maximum position
    /// in _pos; leave vector unchanged
    // inline Scalar maxNorm(int& _pos) const {
    //     Scalar sMax = absolute(m_value[0]);
    //     int    iMax = 0;

    //     for (int i=1;i<N;++i) {
    //         Scalar a=absolute(m_value[i]);
    //         if (a>sMax) {
    //             sMax=a;
    //             iMax=i;
    //         }
    //     }
    //     _pos=iMax;
    //     return sMax;
    // }

    /// compute maximum norm; leave vector unchanged
    // inline Scalar maxNorm() const {
    //     int pos;
    //     return maxNorm(pos);
    // }

    /// normalize vector, return normalized vector
    inline Vector< Scalar, DIM > & normalize()
    {
        Scalar const n = norm();
        assert(n != Scalar(0));
        *this *= Scalar(1)/n;
        return *this;
    }

    // /// return the maximal component
    // inline Scalar max_component() const
    // {
    //     Scalar m;
    //     bool first=true;
    //     for(int i=0; i<N; i++)
    //         if(first) { m=m_value[i]; first=false; }
    //         else if(m_value[i]>m) m=m_value[i];
    //     return m;
    // }

    // /// return the minimal component
    // inline Scalar min_component() const
    // {
    //     Scalar m;
    //     bool first=true;
    //     for(int i=0; i<N; i++)
    //         if(first) { m=m_value[i]; first=false; }
    //         else if(m_value[i]<m) m=m_value[i];
    //     return m;
    // }

    // /// component-wise min
    // inline Vector< Scalar, DIM > min(const Vector< Scalar, DIM > &rhs) {
    //     Vector< Scalar, DIM > res;
    //     for (int i = 0; i < N; i++)
    //         res[i] = std::min(m_value[i],rhs[i]);
    //     return res;
    // }

    // /// component-wise max
    // inline Vector< Scalar, DIM > max(const Vector< Scalar, DIM > &rhs) {
    //     Vector< Scalar, DIM > res;
    //     for (int i = 0; i < N; i++)
    //         res[i] = std::max(m_value[i],rhs[i]);
    //     return res;
    // }

    /// compute scalar product with anrhs vector of same type
    inline Scalar dot(const Vector< Scalar, DIM > & rhs) const
    {
        Scalar dotprd(0.0);
        for(int i = 0; i < DIM; ++i){
            dotprd += m_value[i] * rhs.m_value[i];
        }
        return dotprd;
    }

    /// component-wise self-multiplication with scalar
    inline const Vector< Scalar, DIM > & operator*=(const Scalar &s)
    {
        for(int i = 0; i < DIM; ++i){
            m_value[i] *= s;
        }
        return *this;
     }

    /// component-wise multiplication with scalar
    inline Vector< Scalar, DIM > operator*(Scalar const & s) const
    {
        Vector< Scalar, DIM > v(*this);
        return v *= s;
    }

    /// component-wise self-multiplication
    // inline const Vector< Scalar, DIM >& operator*=(const Vector< Scalar, DIM > &rhs) {
    //     for(int i=0; i<N; i++) m_value[i] *= rhs[i]; return *this; }

    /// component-wise multiplication
    // inline Vector< Scalar, DIM > operator*(const Vector< Scalar, DIM > &rhs) const {
    //     Vector< Scalar, DIM > v(*this); return v*=rhs; }

    /// component-wise self-division by scalar
    // inline const Vector< Scalar, DIM > &operator/=(const Scalar &s) {
    //     for(int i=0; i<N; i++) m_value[i] /= s; return *this; }

    /// component-wise division by scalar
    // inline Vector< Scalar, DIM > operator/(const Scalar &s) const {
    //     Vector< Scalar, DIM > v(*this); return v/=s; }

    /// component-wise self-division
    // inline const Vector< Scalar, DIM > &operator/=(const Vector< Scalar, DIM > &rhs) {
    //     for(int i=0; i<N; i++) m_value[i] /= rhs[i]; return *this; }

    /// component-wise division
    // inline Vector< Scalar, DIM > operator/(const Vector< Scalar, DIM > &rhs) const {
    //     Vector< Scalar, DIM > v(*this); return v/=rhs; }

    /// vector difference from this
    inline Vector< Scalar, DIM > & operator-=(Vector< Scalar, DIM > const & rhs)
    {
        for(int i = 0; i < DIM; ++i){
            m_value[i] -= rhs.m_value[i];
        }
        return *this;
    }

    /// vector difference
    inline Vector< Scalar, DIM > operator-(Vector< Scalar, DIM > const & rhs) const
    {
        Vector< Scalar, DIM > v(*this); v -= rhs;
        return v;
    }

    /// vector self-addition. *this is updated.
    /// \param[in] rhs right hand side
    /// \return computation result
    inline Vector< Scalar, DIM > & operator+=(Vector< Scalar, DIM > const & rhs)
    {
        for(int i = 0; i < DIM; ++i)
        {
            m_value[i] += rhs.m_value[i];
        }
        return *this;
    }

    /// vector addition
    /// \param[in] rhs right hand side
    /// \return computation result
    inline Vector< Scalar, DIM > operator+(const Vector< Scalar, DIM > &rhs) const
    {
        Vector< Scalar, DIM > v(*this);
        v += rhs;
        return v;
    }

    /// unary minus
    inline Vector< Scalar, DIM > operator-() const
    {
        Vector< Scalar, DIM > v(*this);
        for(int i = 0; i < DIM; ++i)
        {
            v.m_value[i] = -v.m_value[i];
        }
        return v;
    }

    /// cross product: only defined for vectors of dimension 3
    /// specialization in one parameter is not possible. This is
    /// friend declaration, this needs forward declaration.
    friend Vector< Scalar, 3 > cross<> (Vector< Scalar, 3 > const & v0,
                                        Vector< Scalar, 3 > const & v1);

    // /** central projection 4D->3D (w=1). this is only defined for 4D. */
    // inline Vector<Scalar,3> centralProjection() const {
    //     assert(!"centralProjection not defined for this type");
    //     return Vector<Scalar,3>(); }

    // /** projects the vector into a plane (3D) normal to the given vector, which
    //     must have unit length. self is modified and the new vector is returned. */
    // inline const Vector< Scalar, DIM >& projectNormalTo(const Vector< Scalar, DIM >& v) {
    //     Scalar sprod = (*this|v);
    //     for(int i=0; i < DIM; ++i) m_value[i] -= (v.m_value[i]*sprod); return *this; }

    // /** component-wise apply function object with Scalar operator()(Scalar). */
    // template<typename func>
    // inline Vector< Scalar, DIM > apply(const func& f) const {
    //     Vector< Scalar, DIM > result;
    //     for(int i=0; i < DIM; ++i) result[i] = f(m_value[i]);
    //     return result; }

private:
    /// The vector value of the template Scalar type.
    Scalar m_value[DIM];
};

/// output a vector by printing its space-separated compontens
template< typename Scalar, int DIM >
inline std::ostream & operator<<(std::ostream & os, Vector< Scalar, DIM > const & vec)
{
    for(int i=0; i < DIM-1; ++i){
        os << vec[i] << " ";
    }
    os << vec[DIM-1];

    return os;
}

/// scalar * Vector
template< typename Scalar, int DIM >
inline Vector< Scalar, DIM > operator*(Scalar s, Vector< Scalar, DIM > const & v )
{
    return v * s;
}

/** read the space-separated components of a vector from a stream */
template<typename Scalar,int DIM>
inline std::istream& operator>>(std::istream & is, Vector< Scalar, DIM > & vec)
{
    for(int i=0; i < DIM; ++i){
        is >> vec[i];
    }
    return is;
}

// /// absolute value (don't dare to name it "abs()")
// template <typename S> inline S absolute(S _s) { return (_s>=S(0)) ? _s : -_s; }
// /// absolute value (don't dare to name it "abs()") for float
// template<> inline float absolute(float _s) { return fabs(_s); }
// /// absolute value (don't dare to name it "obs()") for double
// template<> inline double absolute(double _s) { return fabs(_s); }


/// Float32_3 norm
template<>
inline Float32
Vector< Float32, 2 >::norm() const
{
    return sqrtf(m_value[0] * m_value[0] + m_value[1] * m_value[1]);
}

/// Float64_2
template<>
inline Float64
Vector< Float64, 2 >::norm() const
{
    return sqrt(m_value[0] * m_value[0] + m_value[1] * m_value[1]);
}

/// Float32_3 norm
template<>
inline Float32
Vector< Float32, 3 >::norm() const
{
    return sqrtf(m_value[0] * m_value[0] +
                 m_value[1] * m_value[1] +
                 m_value[2] * m_value[2]);
}

/// Float64_3
template<>
inline Float64
Vector< Float64, 3 >::norm() const
{
    return sqrt(m_value[0] * m_value[0] +
                m_value[1] * m_value[1] +
                m_value[2] * m_value[2]);
}

// /** Vec3 long Float64 norm. */
// template<>
// inline long Float64
// Vector<long Float64,3>::norm() const
// {
//     return sqrt(m_value[0]*m_value[0] +
//                 m_value[1]*m_value[1] +
//                 m_value[2]*m_value[2]);
// }

/// Float32_4 norm
template<>
inline Float32
Vector< Float32, 4 >::norm() const
{
    return sqrtf(m_value[0] * m_value[0] +
                 m_value[1] * m_value[1] +
                 m_value[2] * m_value[2] +
                 m_value[3] * m_value[3]);
}

/// Float64_4 norm
template<>
inline Float64
Vector< Float64, 4 >::norm() const
{
    return sqrt(m_value[0] * m_value[0] +
                m_value[1] * m_value[1] +
                m_value[2] * m_value[2] +
                m_value[3] * m_value[3]);
}

/// Float32_2 sqrnorm
template<>
inline Float32
Vector< Float32, 2 >::sqrnorm() const
{
    return (m_value[0] * m_value[0] +
            m_value[1] * m_value[1]);
}

/// Float64_2 sqrnorm
template<>
inline Float64
Vector< Float64, 2 >::sqrnorm() const
{
    return (m_value[0] * m_value[0] +
            m_value[1] * m_value[1]);
}

/// Float32_3 sqrnorm
template<>
inline Float32
Vector< Float32, 3 >::sqrnorm() const
{
    return(m_value[0] * m_value[0] +
           m_value[1] * m_value[1] +
           m_value[2] * m_value[2]);
}

/// FLoat64_3 sqrnorm
template<>
inline Float64
Vector< Float64, 3 >::sqrnorm() const
{
    return(m_value[0] * m_value[0] +
           m_value[1] * m_value[1] +
           m_value[2] * m_value[2]);
}

/// Float32_4 sqrnorm
template<>
inline Float32
Vector< Float32, 4 >::sqrnorm() const
{
    return(m_value[0] * m_value[0] +
           m_value[1] * m_value[1] +
           m_value[2] * m_value[2] +
           m_value[3] * m_value[3]);
}

/// Float64_4 sqrnorm
template<>
inline Float64
Vector< Float64, 4 >::sqrnorm() const
{
    return(m_value[0] * m_value[0] +
           m_value[1] * m_value[1] +
           m_value[2] * m_value[2] +
           m_value[3] * m_value[3]);
}

//----------------------------------------------------------------------

/// cross product: only defined for Float32_3, Float64_3
template< typename Scalar >
inline Vector< Scalar, 3 > cross(Vector< Scalar, 3 > const & v0,
                                 Vector< Scalar, 3 > const & v1)
{
    return Vector< Scalar, 3 >(
        v0.m_value[1] * v1.m_value[2] - v0.m_value[2] * v1.m_value[1],
        v0.m_value[2] * v1.m_value[0] - v0.m_value[0] * v1.m_value[2],
        v0.m_value[0] * v1.m_value[1] - v0.m_value[1] * v1.m_value[0]);
}

/// central projection for Float32_4
// template<>
// inline Vector<Float32,3>
// Vector<Float32,4>::centralProjection() const {

//     return (fabsf(m_value[3]) > 1e-5) ?
//         Vector<Float32,3>( m_value[0]/m_value[3],
//                          m_value[1]/m_value[3],
//                          m_value[2]/m_value[3]) : Vector<Float32,3>(0.,0.,0.);
// }

// /** central projection for Float64_4 */
// template<>
// inline Vector<Float64,3>
// Vector<Float64,4>::centralProjection() const {

//     return (fabs(m_value[3]) > 1e-5) ?
//         Vector<Float64,3>( m_value[0]/m_value[3],
//                           m_value[1]/m_value[3],
//                           m_value[2]/m_value[3]) : Vector<Float64,3>(0.,0.,0.);
// }

/// compute scalar product with another vector of same type
template<>
inline Float32
Vector< Float32, 3 >::dot(Vector< Float32, 3 > const & rhs) const
{
    return m_value[0] * rhs[0] + m_value[1] * rhs[1] + m_value[2] * rhs[2];
}

// /** add direction (DIM-1) to a DIM vector. ret = p + d*t. Only valid for
//     homogenous points (4D) and 3D direction vector */
// template<typename Scalar>
// inline Vector<Scalar,4> add_direction(const Vector<Scalar,4>& p,
// 				      const Vector<Scalar,3>& d,
// 				      Scalar t=1.0) {
//     Vector<Scalar,4> p_tmp(p);
//     p_tmp.centralProjection();
//     p_tmp[0] += d[0]*t;
//     p_tmp[1] += d[1]*t;
//     p_tmp[2] += d[2]*t;
//     return p_tmp;
// }


/** \name typedefs fr specific case */
//@{
// /// 1-byte signed vector
// typedef Vector<signed char,1> Vec1c;
// /// 1-byte unsigned vector
// typedef Vector<unsigned char,1> Vec1uc;
// /// 1-short signed vector
// typedef Vector<signed short int,1> Vec1s;
// /// 1-short unsigned vector
// typedef Vector<unsigned short int,1> Vec1us;
// /// 1-int signed vector
// typedef Vector<signed int,1> Vec1i;
// /// 1-int unsigned vector
// typedef Vector<unsigned int,1> Vec1ui;
// /// 1-Float32 vector
// typedef Vector<Float32,1> Vec1f;
// /// 1-Float64 vector
// typedef Vector<Float64,1> Vec1d;

/// 2-byte signed vector
// typedef Vector<signed char,2> Vec2c;
// /// 2-byte unsigned vector
// typedef Vector<unsigned char,2> Vec2uc;
// /// 2-short signed vector
// typedef Vector<signed short int,2> Vec2s;
// /// 2-short unsigned vector
// typedef Vector<unsigned short int,2> Vec2us;
// /// 2-int signed vector
// typedef Vector<signed int,2> Vec2i;
// /// 2-int unsigned vector
// typedef Vector<unsigned int,2> Vec2ui;
/// 2-Float32 vector
typedef Vector<Float32,2> Float32_2;
/// 2-Float64 vector
typedef Vector<Float64,2> Float64_2;

/// 3-byte signed vector
// typedef Vector<signed char,3> Vec3c;
// /// 3-byte unsigned vector
// typedef Vector<unsigned char,3> Vec3uc;
// /// 3-short signed vector
// typedef Vector<signed short int,3> Vec3s;
// /// 3-short unsigned vector
// typedef Vector<unsigned short int,3> Vec3us;
// /// 3-int signed vector
// typedef Vector<signed int,3> Vec3i;
// /// 3-int unsigned vector
// typedef Vector<unsigned int,3> Vec3ui;
/// 3-Float32 vector
typedef Vector< Float32, 3 > Float32_3;
/// 3-Float64 vector
typedef Vector<Float64,3> Float64_3;

// /// 4-byte signed vector
// typedef Vector<signed char,4> Vec4c;
// /// 4-byte unsigned vector
// typedef Vector<unsigned char,4> Vec4uc;
// /// 4-short signed vector
// typedef Vector<signed short int,4> Vec4s;
// /// 4-short unsigned vector
// typedef Vector<unsigned short int,4> Vec4us;
// /// 4-int signed vector
// typedef Vector<signed int,4> Vec4i;
// /// 4-int unsigned vector
// typedef Vector<unsigned int,4> Vec4ui;
/// 4-Float32 vector
typedef Vector<Float32,4> Float32_4;
/// 4-Float64 vector
typedef Vector<Float64,4> Float64_4;


/// Color definition
typedef Vector<Float32,4> Color;


//@}
} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_VECTOR_HH
