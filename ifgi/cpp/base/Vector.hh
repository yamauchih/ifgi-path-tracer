//----------------------------------------------------------------------
// ifgi c++ implementation: Vector.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
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
template< typename ScalarType, int DIM > class Vector;
template< typename ScalarType >
Vector<ScalarType,3> cross(Vector<ScalarType,3> const & v0,
                       Vector<ScalarType,3> const & v1);

//----------------------------------------------------------------------

/// A vector is an array of size DIM of type ScalarType
template< typename ScalarType, int DIM >
class Vector {
public:
    /// the type of the scalar used in this template
    typedef ScalarType value_type;
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
    explicit inline Vector(ScalarType const & v0)
    {
        assert(DIM == 1);
        m_value[0] = v0;
    }

    /// constructor with 2 explicit values. only valid for 2 DIM
    /// \param[in] v0 v0 component of vector
    /// \param[in] v1 v1 component of vector
    explicit inline Vector(ScalarType const & v0, ScalarType const & v1)
    {
        assert(DIM == 2);
        m_value[0] = v0;
        m_value[1] = v1;
    }

    /// constructr with 3 explicit values. only valid for 3 DIM
    /// \param[in] v0 v0 component of vector
    /// \param[in] v1 v1 component of vector
    /// \param[in] v2 v2 component of vector
    explicit inline Vector(ScalarType const & v0, ScalarType const & v1,
                           ScalarType const & v2)
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
    explicit inline Vector(ScalarType const & v0, ScalarType const & v1,
                           ScalarType const & v2, ScalarType const & v3)
    {
        assert(DIM == 4);
        m_value[0] = v0;
        m_value[1] = v1;
        m_value[2] = v2;
        m_value[3] = v3;
    }

    /// Construct from a value array
    // explicit inline Vector(const ScalarType value[DIM])
    // {
    //     memcpy(m_value, m_value, DIM * sizeof(ScalarType));
    // }

    /// copy constructor (same kind of vector)
    /// \param[in] rhs right hand side
    inline Vector(Vector< ScalarType, DIM > const &rhs)
    {
        this->operator=(rhs);
    }

    /// operator=
    /// \param[in] rhs right hand side
    inline Vector< ScalarType, DIM > &operator=(Vector< ScalarType, DIM > const & rhs)
    {
        if(&rhs != this){
            memcpy(m_value, rhs.m_value, DIM * sizeof(ScalarType));
        }
        return *this;
    }

    /// get idx'th element read-write
    /// \param[in] idx right hand side
    inline ScalarType & operator[](int idx)
    {
        assert((idx >= 0) && (idx < DIM));
        return m_value[idx];
    }

    /// get idx'th element read-only
    inline ScalarType const & operator[](int idx) const
    {
        assert((idx >= 0) && (idx < DIM));
        return m_value[idx];
    }

    /// compose vector containing the same value in each component
    // static inline Vector< ScalarType, DIM > vectorize(ScalarType value) {
    //     Vector< ScalarType, DIM > result;
    //     for(int i=0; i<N; i++)
    //         result[i] = value;
    //     return result;
    // }

    /// component-wise comparison
    inline bool operator==(Vector< ScalarType, DIM> const & rhs) const
    {
        for(int i = 0; i < DIM; ++i){
            if(m_value[i] != rhs.m_value[i]){
                return false;
            }
        }
        return true;
    }

    /// component-wise comparison
    inline bool operator!=(Vector< ScalarType, DIM > const & rhs) const
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
    inline ScalarType norm() const
    {
        return((ScalarType)sqrt((double)this->sqrnorm()));
    }

    /// get squared norm of the vector
    /// \return squared norm of the vector
    inline ScalarType sqrnorm() const
    {
        return this->dot(*this);
    }

    /// compute maximum norm (absolute value), return maximum position
    /// in _pos; leave vector unchanged
    // inline ScalarType maxNorm(int& _pos) const {
    //     ScalarType sMax = absolute(m_value[0]);
    //     int    iMax = 0;

    //     for (int i=1;i<N;++i) {
    //         ScalarType a=absolute(m_value[i]);
    //         if (a>sMax) {
    //             sMax=a;
    //             iMax=i;
    //         }
    //     }
    //     _pos=iMax;
    //     return sMax;
    // }

    /// compute maximum norm; leave vector unchanged
    // inline ScalarType maxNorm() const {
    //     int pos;
    //     return maxNorm(pos);
    // }

    /// normalize vector, return normalized vector
    inline Vector< ScalarType, DIM > & normalize()
    {
        ScalarType const n = norm();
        assert(n != ScalarType(0));
        *this *= ScalarType(1)/n;
        return *this;
    }

    // /// return the maximal component
    // inline ScalarType max_component() const
    // {
    //     ScalarType m;
    //     bool first=true;
    //     for(int i=0; i<N; i++)
    //         if(first) { m=m_value[i]; first=false; }
    //         else if(m_value[i]>m) m=m_value[i];
    //     return m;
    // }

    // /// return the minimal component
    // inline ScalarType min_component() const
    // {
    //     ScalarType m;
    //     bool first=true;
    //     for(int i=0; i<N; i++)
    //         if(first) { m=m_value[i]; first=false; }
    //         else if(m_value[i]<m) m=m_value[i];
    //     return m;
    // }

    // /// component-wise min
    // inline Vector< ScalarType, DIM > min(const Vector< ScalarType, DIM > &rhs) {
    //     Vector< ScalarType, DIM > res;
    //     for (int i = 0; i < N; i++)
    //         res[i] = std::min(m_value[i],rhs[i]);
    //     return res;
    // }

    // /// component-wise max
    // inline Vector< ScalarType, DIM > max(const Vector< ScalarType, DIM > &rhs) {
    //     Vector< ScalarType, DIM > res;
    //     for (int i = 0; i < N; i++)
    //         res[i] = std::max(m_value[i],rhs[i]);
    //     return res;
    // }

    /// compute scalar product with anrhs vector of same type
    inline ScalarType dot(const Vector< ScalarType, DIM > & rhs) const
    {
        ScalarType dotprd(0.0);
        for(int i = 0; i < DIM; ++i){
            dotprd += m_value[i] * rhs.m_value[i];
        }
        return dotprd;
    }

    /// component-wise self-multiplication with scalar
    inline const Vector< ScalarType, DIM > & operator*=(const ScalarType &s)
    {
        for(int i = 0; i < DIM; ++i){
            m_value[i] *= s;
        }
        return *this;
     }

    /// component-wise multiplication with scalar
    inline Vector< ScalarType, DIM > operator*(ScalarType const & s) const
    {
        Vector< ScalarType, DIM > v(*this);
        return v *= s;
    }

    /// component-wise self-multiplication
    inline const Vector< ScalarType, DIM >& operator*=(Vector< ScalarType, DIM > const & rhs)
    {
        for(int i = 0; i < DIM; i++){
            m_value[i] *= rhs[i];
        }
        return *this;
    }

    /// component-wise multiplication
    inline Vector< ScalarType, DIM > operator*(const Vector< ScalarType, DIM > &rhs) const
    {
        Vector< ScalarType, DIM > v(*this);
        return v *= rhs;
    }

    /// component-wise self-division by scalar
    inline const Vector< ScalarType, DIM > &operator/=(const ScalarType &s)
    {
        assert(s != ScalarType(0.0));
        for(int i=0; i < DIM; ++i){
            m_value[i] /= s;
        }
        return *this;
    }

    /// component-wise division by scalar
    inline Vector< ScalarType, DIM > operator/(const ScalarType &s) const
    {
        Vector< ScalarType, DIM > v(*this);
        return v /= s;
    }

    /// component-wise self-division
    inline const Vector< ScalarType, DIM > &operator/=(const Vector< ScalarType, DIM > &rhs)
    {
        for(int i = 0; i < DIM; ++i){
            m_value[i] /= rhs[i];
        }
        return *this;
    }

    /// component-wise division
    inline Vector< ScalarType, DIM > operator/(const Vector< ScalarType, DIM > &rhs) const
    {
        Vector< ScalarType, DIM > v(*this);
        return v/=rhs;
    }

    /// vector difference from this
    inline Vector< ScalarType, DIM > & operator-=(Vector< ScalarType, DIM > const & rhs)
    {
        for(int i = 0; i < DIM; ++i){
            m_value[i] -= rhs.m_value[i];
        }
        return *this;
    }

    /// vector difference
    inline Vector< ScalarType, DIM > operator-(Vector< ScalarType, DIM > const & rhs) const
    {
        Vector< ScalarType, DIM > v(*this); v -= rhs;
        return v;
    }

    /// vector self-addition. *this is updated.
    /// \param[in] rhs right hand side
    /// \return computation result
    inline Vector< ScalarType, DIM > & operator+=(Vector< ScalarType, DIM > const & rhs)
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
    inline Vector< ScalarType, DIM > operator+(const Vector< ScalarType, DIM > &rhs) const
    {
        Vector< ScalarType, DIM > v(*this);
        v += rhs;
        return v;
    }

    /// unary minus
    inline Vector< ScalarType, DIM > operator-() const
    {
        Vector< ScalarType, DIM > v(*this);
        for(int i = 0; i < DIM; ++i)
        {
            v.m_value[i] = -v.m_value[i];
        }
        return v;
    }

    /// cross product: only defined for vectors of dimension 3
    /// specialization in one parameter is not possible. This is
    /// friend declaration, this needs forward declaration.
    friend Vector< ScalarType, 3 > cross<> (Vector< ScalarType, 3 > const & v0,
                                        Vector< ScalarType, 3 > const & v1);

    // /** central projection 4D->3D (w=1). this is only defined for 4D. */
    // inline Vector<ScalarType,3> centralProjection() const {
    //     assert(!"centralProjection not defined for this type");
    //     return Vector<ScalarType,3>(); }

    // /** projects the vector into a plane (3D) normal to the given vector, which
    //     must have unit length. self is modified and the new vector is returned. */
    // inline const Vector< ScalarType, DIM >& projectNormalTo(const Vector< ScalarType, DIM >& v) {
    //     ScalarType sprod = (*this|v);
    //     for(int i=0; i < DIM; ++i) m_value[i] -= (v.m_value[i]*sprod); return *this; }

    // /** component-wise apply function object with ScalarType operator()(ScalarType). */
    // template<typename func>
    // inline Vector< ScalarType, DIM > apply(const func& f) const {
    //     Vector< ScalarType, DIM > result;
    //     for(int i=0; i < DIM; ++i) result[i] = f(m_value[i]);
    //     return result; }

private:
    /// The vector value of the template ScalarType type.
    ScalarType m_value[DIM];
};

/// output a vector by printing its space-separated compontens
template< typename ScalarType, int DIM >
inline std::ostream & operator<<(std::ostream & os, Vector< ScalarType, DIM > const & vec)
{
    for(int i=0; i < DIM-1; ++i){
        os << vec[i] << " ";
    }
    os << vec[DIM-1];

    return os;
}

/// scalar * Vector
template< typename ScalarType, int DIM >
inline Vector< ScalarType, DIM > operator*(ScalarType s, Vector< ScalarType, DIM > const & v )
{
    return v * s;
}

/** read the space-separated components of a vector from a stream */
template<typename ScalarType,int DIM>
inline std::istream& operator>>(std::istream & is, Vector< ScalarType, DIM > & vec)
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
template< typename ScalarType >
inline Vector< ScalarType, 3 > cross(Vector< ScalarType, 3 > const & v0,
                                 Vector< ScalarType, 3 > const & v1)
{
    return Vector< ScalarType, 3 >(
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
// template<typename ScalarType>
// inline Vector<ScalarType,4> add_direction(const Vector<ScalarType,4>& p,
// 				      const Vector<ScalarType,3>& d,
// 				      ScalarType t=1.0) {
//     Vector<ScalarType,4> p_tmp(p);
//     p_tmp.centralProjection();
//     p_tmp[0] += d[0]*t;
//     p_tmp[1] += d[1]*t;
//     p_tmp[2] += d[2]*t;
//     return p_tmp;
// }


/// \name typedefs fr specific case
//@{

/// Sint8 vector 2
typedef Vector< Sint8,   2 > Sint8_2;
/// Sint8 vector 3
typedef Vector< Sint8,   3 > Sint8_3;
/// Sint8 vector 4
typedef Vector< Sint8,   4 > Sint8_4;

/// Uint8 vector 2
typedef Vector< Uint8,   2 > Uint8_2;
/// Uint8 vector 3
typedef Vector< Uint8,   3 > Uint8_3;
/// Uint8 vector 4
typedef Vector< Uint8,   4 > Uint8_4;

/// Sint16 vector 2
typedef Vector< Sint16,  2 > Sint16_2;
/// Sint16 vector 3
typedef Vector< Sint16,  3 > Sint16_3;
/// Sint16 vector 4
typedef Vector< Sint16,  4 > Sint16_4;


/// Uint16 vector 2
typedef Vector< Uint16,  2 > Uint16_2;
/// Uint16 vector 3
typedef Vector< Uint16,  3 > Uint16_3;
/// Uint16 vector 4
typedef Vector< Uint16,  4 > Uint16_4;


/// Sint32 vector 2
typedef Vector< Sint32,  2 > Sint32_2;
/// Sint32 vector 3
typedef Vector< Sint32,  3 > Sint32_3;
/// Sint32 vector 4
typedef Vector< Sint32,  4 > Sint32_4;


/// Uint32 vector 2
typedef Vector< Uint32,  2 > Uint32_2;
/// Uint32 vector 3
typedef Vector< Uint32,  3 > Uint32_3;
/// Uint32 vector 4
typedef Vector< Uint32,  4 > Uint32_4;


/// Sint64 vector 2
typedef Vector< Sint64,  2 > Sint64_2;
/// Sint64 vector 3
typedef Vector< Sint64,  3 > Sint64_3;
/// Sint64 vector 4
typedef Vector< Sint64,  4 > Sint64_4;


/// Uint64 vector 2
typedef Vector< Uint64,  2 > Uint64_2;
/// Uint64 vector 3
typedef Vector< Uint64,  3 > Uint64_3;
/// Uint64 vector 4
typedef Vector< Uint64,  4 > Uint64_4;


/// Float32 vector 2
typedef Vector< Float32, 2 > Float32_2;
/// Float32 vector 3
typedef Vector< Float32, 3 > Float32_3;
/// Float32 vector 4
typedef Vector< Float32, 4 > Float32_4;


/// Float64 vector 2
typedef Vector< Float64, 2 > Float64_2;
/// Float64 vector 3
typedef Vector< Float64, 3 > Float64_3;
/// Float64 vector 4
typedef Vector< Float64, 4 > Float64_4;


/// ScalarType vector 2
typedef Vector< Scalar, 2 > Scalar_2;
/// Scalar vector 3
typedef Vector< Scalar, 3 > Scalar_3;
/// Scalar vector 4
typedef Vector< Scalar, 4 > Scalar_4;


/// Color definition
typedef Scalar_4 Color;

//@}
} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_VECTOR_HH
