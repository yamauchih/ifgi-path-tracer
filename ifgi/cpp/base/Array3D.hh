//----------------------------------------------------------------------
// ifgi c++ implementation: Array3D.hh
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief resizable 3D array based on imgsynth
#ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_ARRAY3D_HH
#define IFGI_PATH_TRACER_IFGI_CPP_BASE_ARRAY3D_HH

#include <cstdio>

#include "Vector.hh"
#include "Dictionary.hh"
#include "Exception.hh"

namespace ifgi
{
/// 3D array with memory management.
///
/// You can put any class to ElementT, but for simple and fast, I
/// recommend to use basic type, like char, int, float, double and so
/// on.
///
/// \param ElementT element of pixel. Usually, float or double.
template< typename ElementT >
class Array3D
{
public:
    /// constructor
    /// generate an invalid channel.
    Array3D()
    {
        this->initAsInvalid();
    }

    /// constructor with buffer allocation.
    /// \param  _xsize x size of this array
    /// \param  _ysize y size of this array
    /// \param  _zsize z size of this array
    Array3D(int _xsize, int _ysize, int _zsize)
    {
        this->initAsInvalid();
        this->reallocBuffer(_xsize, _ysize, _zsize);
    }

    /// constructor with buffer allocation.
    /// \param _dim size of the buffer
    Array3D(const Sint32_3 & _dim)
    {
        this->initAsInvalid();
        this->reallocBuffer(_dim[0], _dim[1], _dim[2]);
    }

    /// constructor with buffer allocation and fill buffer as initval.
    ///
    /// \param  _xsize  x size of this array
    /// \param  _ysize  y size of this array
    /// \param  _zsize  z size of this array
    /// \param _initval initialize value (the buffer is filled with
    /// this value.)
    Array3D(int _xsize, int _ysize, int _zsize, const ElementT& _initval)
    {
        this->initAsInvalid();
        this->reallocBuffer(_xsize, _ysize, _zsize);
        this->clearWithValue(_initval);
    }

    /// constructor with buffer allocation.
    /// \param  _dim size of the buffer
    /// \param _initval initialize value (the buffer is filled with
    /// this value.)
    Array3D(const Sint32_3& _dim, const ElementT& _initval)
    {
        this->initAsInvalid();
        this->reallocBuffer(_dim[0], _dim[1], _dim[2]);
        this->clearWithValue(_initval);
    }

    /// copy constructor
    /// \param _rhs construct with rhs(source Array3D).
    Array3D(const Array3D< ElementT >& _rhs)
    {
        this->initAsInvalid();
        this->reallocBuffer(_rhs.d_xsize, _rhs.d_ysize, _rhs.d_zsize);
        this->overrideCopy(_rhs);
    }

    /// substition
    /// \param _rhs substitute with _rhs(source Array3D).
    const Array3D< ElementT > & operator=(const Array3D< ElementT > & _rhs)
    {
        if(this != &_rhs){
            this->reallocBuffer(_rhs.d_xsize, _rhs.d_ysize, _rhs.d_zsize);
            this->overrideCopy(_rhs);
        }
        return(*this);
    }

    /// destructor
    virtual ~Array3D()
    {
        if(d_pBuffer != 0){
            delete [] d_pBuffer;
            d_pBuffer = 0;
        }
        d_xsize = -1;
        d_ysize = -1;
        d_zsize = -1;
    }

    /// resize the buffer
    /// The content image will be invalid when size is changed.
    /// \param _newXsize new size of X
    /// \param _newYsize new size of Y
    /// \param _newZsize new size of Z
    void resizeBuffer(int _newXsize, int _newYsize, int _newZsize){
        if((this->getXSize() != _newXsize) ||
           (this->getYSize() != _newYsize) ||
           (this->getZSize() != _newZsize))
        {
            this->reallocBuffer(_newXsize, _newYsize, _newZsize);
        }
    }

    /// resize the buffer with Dimension
    /// \param _dim x, y, z size
    void resizeBuffer(const Sint32_3& _dim){
        this->resizeBuffer(_dim[0], _dim[1], _dim[2]);
    }

    /// set a content, index is raw index @see A3DIdxMappable.hh
    /// override a pixel with a value
    /// \param _x index of x
    /// \param _y index of y
    /// \param _z index of z
    /// \param _value a value at x,y,z.
    inline void set(int _x, int _y, int _z, const ElementT& _value){
        if(this->isValidPosition(_x, _y, _z)){
            d_pBuffer[this->getIdx(_x, _y, _z)] = _value;
        }
        else{
            this->outInvalidRangeWarn(_x, _y, _z, "set", "set is ignored.");
        }
    }
    /// set with Sint32_3
    inline void set(const Sint32_3& _p, const ElementT& _value){
        this->set(_p[0], _p[1], _p[2], _value);
    }

    /// peek a content, index is raw index @see A3DIdxMappable.hh
    /// This may faster than get in some case.
    /// \param _x index of x
    /// \param _y index of y
    /// \param _z index of z
    /// \return reference of value at _x, _y, _z.
    inline ElementT* peek(int _x, int _y, int _z){
        if(this->isValidPosition(_x, _y, _z)){
            return(&(d_pBuffer[this->getIdx(_x, _y, _z)]));
        }
        else {
            static ElementT peekdummy;
            this->outInvalidRangeWarn(_x, _y, _z, "peek",
                                      "peek returns a reference as ElementT() = " +
                                      Dictionary_value(peekdummy).get< std::string >());
            return(&peekdummy);
        }
    }

    /// peek with Sint32_3
    inline ElementT* peek(const Sint32_3& _p)
    {
        return(this->peek(_p[0], _p[1], _p[2]));
    }

    /// get a content, index is raw index @see A3DIdxMappable.hh
    /// \param _x index of x
    /// \param _y index of y
    /// \param _z index of z
    /// \return the value at index _x, _y, _z.
    inline ElementT get(int _x, int _y, int _z) const {
        if(this->isValidPosition(_x, _y, _z)) {
            return(d_pBuffer[this->getIdx(_x, _y, _z)]);
        }
        else {
            std::stringstream sstr;
            static ElementT dummyget;
            sstr << dummyget;
            this->outInvalidRangeWarn(_x, _y, _z, "get",
                                      std::string("get returns ElementT = ") +
                                      sstr.str());
            return(dummyget);
        }
    }
    /// get with Sint32_3
    inline ElementT get(const Sint32_3& _p) const {
        return(this->get(_p[0], _p[1], _p[2]));
    }

    /// get size x of this array
    /// \return size of X
    inline int getXSize() const {
        return(d_xsize);
    }

    /// get size y of this array
    /// \return size of Y
    inline int getYSize() const {
        return(d_ysize);
    }

    /// get size z of this array
    /// \return size of Z
    inline int getZSize() const {
        return(d_zsize);
    }

    /// get dimension (size of array) with 3D
    /// \return dimension x, y, z
    inline Sint32_3 getDimension() const {
        return(Sint32_3(this->getXSize(), this->getYSize(), this->getZSize()));
    }

    /// clear with a value
    /// \param clearValue fill whole buffer with this clearValue
    /// @see A3DClearWithColor the idea ``color'' is a special idea when
    /// Array3D is thought as image. So, the routine is not here but
    /// in Array3DUtil.
    void clearWithValue(const ElementT& clearValue) {
        if(d_pBuffer == NULL) {
            std::cerr << "Error! : Array3D::clearWithValue : "
                      << "No buffer is allocated. Ignored." << std::endl;
            return;
        }

        for(int i = 0; i < this->getVolume(); i++) {
            d_pBuffer[i] = clearValue;
        }
    }

    /// isValid?
    bool isValid() const {
        if((d_xsize > 0) && (d_ysize > 0) && (d_zsize > 0) &&
           (d_pBuffer != NULL)) {
            return(true);
        }
        else{
            return(false);
        }
    }

    /// is valid position
    inline bool isValidPosition(const int x, const int y, const int z) const {
        if((0 <= x) && (x < d_xsize) &&
           (0 <= y) && (y < d_ysize) &&
           (0 <= z) && (z < d_zsize)) {
            return(true);
        }
        else {
            return(false);
        }
    }

    /// is equal dimension
    /// \return true iff both size of each dimension are the same.
    bool isEqualDimension(Array3D< ElementT >* _pRhs) const {
        if((this->isValid() == false) || (_pRhs->isValid() == false)) {
            std::stringstream sstr;
            sstr << "Error! : Array3D<T>::equalDimension : invalid array.";
            throw Exception(sstr.str());
        }
        if((d_xsize == _pRhs->d_xsize) && (d_ysize == _pRhs->d_ysize) &&
           (d_zsize == _pRhs->d_zsize)) {
            return(true);
        }
        else {
            return(false);
        }
    }

    /// peek the buffer array.
    ///
    /// This is a dangerous operation. This gives the top address of the
    /// internal image buffer. You should keep the consistency. For
    /// example, when the buffer is resized, the pointer may not valid
    /// anymore.
    ///
    /// This is useful for rendering an Array3D by OpenGL. OpenGL
    /// glDrawPixels() can directory use this buffer, since we implement
    /// the Array3D which has the order buffer[Y][X][Z(RGB)].
    ///
    /// \return reference of the top of buffer address.
    inline ElementT* peekDataArray() {
        assert(d_pBuffer != 0);
        return(d_pBuffer);
    }

    /// std::string representation
    /// \return std::string representation of this instance
    std::string toString() const {
        char buf[256];
        std::string r = "";
        if(d_xsize > 0){
            snprintf(buf, 256, "size (%d %d %d)",
                     d_xsize, d_ysize, d_zsize);
            r += std::string(buf);
            return(r);
        }
        else{
            return(std::string("Array3D::toString : array is not initialized."));
        }
    }

    /// write all data to a stream.
    ///
    /// \param  os        output stream
    /// \param  prefix    prefix  string of output
    /// \param  postfix   postfix string of output
    /// \param  isOutEndl when change the dimension, output std::endl
    /// \return false if this array is not initialized
    bool write(std::ostream &os,
               const std::string& prefix,
               const std::string& postfix,
               const bool isOutEndl = true) const {
        if(d_xsize > 0) {
            for(int z = 0; z < this->getZSize(); z++) {
                for(int y = 0; y < this->getYSize(); y++) {
                    for(int x = 0; x < this->getXSize(); x++) {
                        os << prefix << this->get(x, y, z) << postfix;
                    }
                    if(isOutEndl) {
                        os << std::endl;
                    }
                }
            }
            return(true);
        }
        else {
            // os << std::string("Array1D::toString : array is not initialized.");
            return(false);
        }
    }

    /// get volume of this array
    /// synonym of size
    /// \return size of buffer
    inline int getVolume() const {
        return this->size();
    }
    /// size of the buffer
    /// \return size of the buffer
    inline int size() const {
        return(d_xsize * d_ysize * d_zsize);
    }

    /// realloc and copy
    ///
    /// Possible reallocate, so if your program see the internel buffer
    /// pointer (e.g., to show the image with OpenGL.) The pointer may be
    /// not valid anymore. But after the copy, the buffer size is always
    /// correct.
    ///
    /// \param _rhs construct with rhs(source Array3D).
    const Array3D< ElementT > & reallocCopy(const Array3D< ElementT >& _rhs){
        if(this != &_rhs){
            this->reallocBuffer(_rhs.d_xsize, _rhs.d_ysize, _rhs.d_zsize);
            this->overrideCopy(_rhs);
        }
        return(*this);
    }

    /// override existing buffer
    ///
    /// Do not reallocate the buffer. Therefore, image size should be the
    /// same. Otherwise throw Exception.
    ///
    /// \param _rhs copy source. destination is *this.
    const Array3D< ElementT > & overrideCopy(const Array3D< ElementT >& _rhs) {
        if((d_xsize != _rhs.d_xsize) || (d_ysize != _rhs.d_ysize) ||
           (d_zsize != _rhs.d_zsize))
        {
            std::stringstream sstr;
            sstr << "Error!: Array3D::overrideCopy : "
                 << "Can not copy buffer since sizes are different.";
            throw Exception(sstr.str());
            return(*this);
        }
        for(int i = 0; i < this->size(); i++) {
            d_pBuffer[i] = _rhs.d_pBuffer[i];
        }
        return(*this);
    }

private:
    /// initialize as not initialized in valid way
    /// This should called only first time.
    void initAsInvalid() {
        d_xsize   = 0;
        d_ysize   = 0;
        d_zsize   = 0;
        d_pBuffer = 0;
    }

    /// get index of buffer contents
    inline int getIdx(int _x, int _y, int _z) const {
#ifndef NDEBUG
        // init test
        if((d_xsize < 0) || (d_ysize < 0) || (d_zsize < 0) ||
           (d_pBuffer == NULL)) {
            std::stringstream sstr;
            sstr << "Error!: Array3D::getIdx : not initialized.";
            throw Exception(sstr.str());
        }
        // index range test
        if(this->isValidPosition(_x, _y, _z) == false) {
            this->outInvalidRangeWarn(_x, _y, _z, "getIdx", "exception.");
            throw Exception("Array3D: Invalid range.");
        }
#endif
        // return(x + d_xsize * (y + z * d_ysize));
        // currentImage2[y * (xsz * zsz) + (x * zsz) + z] = a3d.get(x,y,z);
        return((_y * d_xsize + _x) * d_zsize + _z);
    }

    /// re-allocate buffer: if buffer is already allocated,
    /// re-allocate. But the dimension is the same, do nothing.
    ///
    /// If one of the size == 0, initialize as invalid and delete buffer
    /// if allocated.
    ///
    /// \param _xsize size of x (>= 0)
    /// \param _ysize size of y (>= 0)
    /// \param _zsize size of z (>= 0)
    void reallocBuffer(int _xsize, int _ysize, int _zsize) {
        if((_xsize < 0) || (_ysize < 0) || (_zsize < 0)) {
            std::cerr << "Error!: Array3D::reallocBuffer(" << _xsize << ", "
                      << _ysize << ", " << _zsize << "), invalid size, not initialized."
                      << std::endl;
            return;
        }

        if(d_pBuffer != 0) {
            delete [] d_pBuffer;
        }
        d_pBuffer = 0;

        d_xsize = _xsize;
        d_ysize = _ysize;
        d_zsize = _zsize;
        if((d_xsize > 0) && (d_ysize > 0) && (d_zsize > 0)){ // only size exists
            d_pBuffer = new ElementT [(d_xsize * d_ysize * d_zsize)];
        }
        else{
            // no size
            d_xsize = 0;
            d_ysize = 0;
            d_zsize = 0;
        }
    }

    /// invalid range warning
    ///
    /// \param x   	position x
    /// \param y   	position y
    /// \param z   	position z
    /// \param methodName  method name
    /// \param mes         message
    void outInvalidRangeWarn(int x, int y, int z,
                             const std::string& methodName,
                             const std::string& mes) const {
#ifndef NDEBUG
        std::cerr << "Warning!: Array3D::" << methodName
                  << "(" << x << ", " << y << ", " << z  << ") is out of range. Size = ("
                  << d_xsize << ", " << d_ysize << ", " << d_zsize << "). "
                  << mes << std::endl;
#endif // #ifndef NDEBUG
    }


    // Next three methods reveals the internal data alignment structure, and
    // hard to keep compatibility. Therefore, they are in private. H.Y.

    /// set a content as 1D Array
    /// override a pixel with a value
    /// \param idx index of the buffer.
    /// \param value a value at idx.
    inline void setAs1D(int idx, const ElementT& value) {
        assert((0 <= idx) && (idx < this->getVolume()));
        d_pBuffer[idx] = value;
    }

    /// peek a content as 1D Array
    /// This may faster than get in some case.
    /// \param idx index of the buffer.
    /// \return reference of value at idx.
    inline ElementT* peekAs1D(int idx) {
        assert((0 <= idx) && (idx < this->getVolume()));
        return(&(d_pBuffer[idx]));
    }

    /// get a content as 1D Array
    /// \param idx index of the buffer
    /// \return the value at index idx.
    inline ElementT getAs1D(int idx) const {
        assert((0 <= idx) && (idx < this->getVolume()));
        return(d_pBuffer[idx]);
    }

private:
    // buffer x size
    int d_xsize;
    // buffer y size
    int d_ysize;
    // buffer z size
    int d_zsize;
    // buffer array, 1-D array. (x,y,z)->idx is done by getIdx()
    ElementT *d_pBuffer;
};

// convenient typedef
/// Float  buffer
typedef Array3D< Float32 > Array3D_Float32;
/// Double buffer
typedef Array3D< Float64 > Array3D_Float64;

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_ARRAY3D_HH
