//----------------------------------------------------------------------
// ifgi c++ implementation: SGMaterialNode.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief scene graph material node

#include "SGMaterialNode.hh"

namespace ifgi
{
//----------------------------------------------------------------------
// constructor
SGMaterialNode::SGMaterialNode(std::string const & nodename)
    :
    SceneGraphNode(nodename),
    m_p_material(0)
{
    // empty
}

//----------------------------------------------------------------------
// get classname
std::string SGMaterialNode::get_classname() const
{
    return "SGMaterialNode";
}

//----------------------------------------------------------------------
// is this a primitive node?
bool SGMaterialNode::is_primitive_node() const
{
    return false;
}

//----------------------------------------------------------------------
// get bounding box of this node
// BBox32 const & SGMaterialNode::get_bbox() const
// {
//     assert(false);
//     return BBox32();
// }

//----------------------------------------------------------------------
// Does this node have a bounding box?
bool SGMaterialNode::has_node_bbox() const
{
    return false;
}

//----------------------------------------------------------------------
// set a material.
void SGMaterialNode::set_material(IMaterial * p_mat)
{
    if(this->has_children()){
        throw Exception("Can not set a material since there are children.");
    }
    if(m_p_material != 0){
        ILog::instance()->warn("SGMaterialNode::set_material: "
                               "override the existing matrial.");
    }
    m_p_material = p_mat;
}

//----------------------------------------------------------------------
// peek the material.
IMaterial * SGMaterialNode::peek_material() const
{
    return m_p_material;
}
//----------------------------------------------------------------------

} // namespace ifgi
