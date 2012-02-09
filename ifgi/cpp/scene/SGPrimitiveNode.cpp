//----------------------------------------------------------------------
// ifgi c++ implementation: SGPrimitiveNode.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief scene graph primitive node

#include "SGPrimitiveNode.hh"

#include <sstream>
#include <cpp/base/ILog.hh>


namespace ifgi
{
//----------------------------------------------------------------------
// constructor
SGPrimitiveNode::SGPrimitiveNode(std::string const & nodename,
                                 IPrimitive * p_prim)
    :
    SceneGraphNode(nodename),
    m_p_prim_ref(p_prim)
{
    // empty
}

//----------------------------------------------------------------------
// get classname
std::string SGPrimitiveNode::get_classname() const
{
    return "SGPrimitiveNode";
}

//----------------------------------------------------------------------
// set nodename (shown in the SceneGraph viewer as Node);
// void SGPrimitiveNode::set_nodename(std::string const & nodename)
// {
//     m_nodename = nodename;
// }

//----------------------------------------------------------------------
// get nodename
// std::string SGPrimitiveNode::get_nodename() const
// {
//     return m_nodename;
// }

//----------------------------------------------------------------------
// Use SceneGraphNode"s method
// def append_child(_child){
//     /// append child
//     \param[in] child child node
//     ///
//     if this->is_primitive_node(){
//         raise StandardError, ("Cannot append a child to a primitive node.");
//     m_children.append(_child);

// get child list
// def get_children(){
//     /// get child list.
//     \return list of children. may None///
//     return m_children


//------------------------------------------------------------
// primitive node interface
//------------------------------------------------------------

// is this a primitive node?
// bool SGPrimitiveNode::is_primitive_node() const
// {
//     assert(m_p_prim_ref != 0);
//     return true;
// }

//----------------------------------------------------------------------
// set a primitive.
void SGPrimitiveNode::set_primitive(IPrimitive * p_prim)
{
    if(this->has_children()){
        throw Exception("Can not set a primitive. already had children.");
    }
    if(m_p_prim_ref != 0){
        ILog::instance()->warn("SGPrimitiveNode::set_primitive: "
                               "This node has a primitive. Override the primitive.");
    }
    m_p_prim_ref = p_prim;
}

//----------------------------------------------------------------------
// get bounding box of this node
BBoxScalar const & SGPrimitiveNode::get_bbox() const
{
    if(m_p_prim_ref == 0){
        throw Exception("No primitive set [" + this->get_classname() +
                        " " + this->get_nodename() + "]");
    }
    return m_p_prim_ref->get_bbox();
}

//----------------------------------------------------------------------
// assign bbox value.
// void SGPrimitiveNode::set_bbox(BBoxScalar const & bbox)
// {
//     m_primitive.set_bbox(bbox);
// }

//----------------------------------------------------------------------
// print this object for debug.
std::string SGPrimitiveNode::get_nodeinfo(Sint32 level)
{
    std::stringstream sstr;
    for(int i = 0; i < level; ++i){
        sstr << "  ";
    }

    sstr << "+ SGPrimitive:" << m_p_prim_ref->get_classname()
         << " " << m_p_prim_ref->get_bbox().to_string();

    return sstr.str();
}

//----------------------------------------------------------------------
} // namespace ifgi
