//----------------------------------------------------------------------
// ifgi c++ implementation: ifgi texture
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief scene element texture

/// import sys
/// import math
/// import numpy

class ITexture
{
    public:
    /// Texture class: interface///

    def __init__(){
        /// default constructor///
        pass


    def get_classname(){
        /// get class name. interface method. (public).
        \return class name
        ///
        assert 0, "get_classname must be implemented in a derived class."
        return None


    def value(_uv, _point){
        /// texture value.

        \param[in] _uv    texture uv coordinate (if surface)
        \param[in] _point texture point in 3d (if solid)
        \return texture color value
        ///
        assert 0, "value must be implemented in a derived class."
        return None


class ConstantColorTexture(Texture){
    /// Constant color texture///

    def __init__(_color){
        /// default constructor

        \param[in] _color constant color float4
        ///
        this->__color = _color


    def get_classname(){
        /// get class name. interface method. (public).
        \return class name
        ///
        return "ConstantColorTexture"


    def set_constant_color(_col){
        /// set constant color.
        \param[in] _col constant color of this texture
        ///
        this->__color = _col


    def value(_uv, _point){
        /// texture value.

        \param[in] _uv    texture uv coordinate (if surface);
        \param[in] _point texture point in 3d (if solid);
        \return texture color value
        ///
        return this->__color


class ImageTexture(object){
    /// Image texture class///

    def __init__(){
        /// default constructor///
        pass


    def get_classname(){
        /// get class name. interface method. (public).
        \return class name
        ///
        assert 0, "get_classname must be implemented in a derived class."
        return None


    def value(_uv, _point){
        /// texture value.

        \param[in] _uv    texture uv coordinate (if surface);
        \param[in] _point texture point in 3d (if solid);
        \return texture color value
        ///
        assert 0, "value must be implemented in a derived class."
        return None
