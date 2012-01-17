//----------------------------------------------------------------------
// ifgi c++ implementation: SGPrimitiveNode.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief scene graph primitive node
#ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_SGPRIMITIVENODE_HH
#define IFGI_PATH_TRACER_IFGI_CPP_SCENE_SGPRIMITIVENODE_HH

#include "SceneGraphNode.hh"

#include <cpp/base/ILog.hh>

namespace ifgi
{
//----------------------------------------------------------------------
// forward declaration
class IPrimitive;

//----------------------------------------------------------------------

/// Primitive node, a Scene Graph Node.
///
/// This has
/// - a primitive also this can have children.
/// - a reference to the material.
/// - a name
/// - a bounding box
/// TriMesh doesn't have many of them.
///
class SGPrimitiveNode : public SceneGraphNode
{
public:
    /// constructor
    /// \param[in] nodename node name
    /// \param[in] p_prim   reference to a IPrimitive
    SGPrimitiveNode(std::string const & nodename,
                    IPrimitive * p_prim);

    /// get classname
    /// \return: scnegraph node class name
    virtual std::string get_classname() const;

    /// set nodename (shown in the SceneGraph viewer as Node);
    /// \param[in] nodename nodename for scenegraph visualization
    // virtual void set_nodename(std::string const & nodename);

    /// get nodename
    /// \return: node (instance) name
    // virtual std::string get_nodename() const;

    /// Use SceneGraphNode"s method
    /// def append_child(_child){
    ///     /// append child
    ///     \param[in] child child node
    ///     ///
    ///     if this->is_primitive_node(){
    ///         raise StandardError, ("Cannot append a child to a primitive node.");
    ///     m_children.append(_child);

    /// get child list
    /// def get_children(){
    ///     /// get child list.
    ///     \return list of children. may None///
    ///     return m_children

public:
    // ------------------------------------------------------------
    // primitive node interface
    // ------------------------------------------------------------

    /// is this a primitive node?
    /// \return True when this node is primitive node.
    ///
    /// This node must have a primitive in run time
    bool is_primitive_node() const
    {
        assert(m_p_prim_ref != 0);
        return true;
    }

    /// set a primitive.
    ///
    /// \param[in] p_prim a primitive
    void set_primitive(IPrimitive * p_prim);

    /// get the primitive.
    ///
    /// Reimplemented in PrimitiveNode.
    ///
    /// \return a assigned primitive.
    IPrimitive * peek_primitive()
    {
        return m_p_prim_ref;
    }

    /// Does this node have a bounding box?
    /// \return True when the node can have a bounding box.
    virtual bool has_node_bbox() const
    {
        return true;
    }

    /// get bounding box of this node
    /// \return bounding box
    BBox32 const & get_bbox() const;

    /// assign bbox value.
    /// set the bbox object. (bbox is cloned before set.);
    /// \param[in] bbox bounding box to be assigned.
    // void set_bbox(BBox32 const & bbox)
    // {
    //     m_p_prim_ref->set_bbox(bbox);
    // }

    /// print this object for debug.
    /// \param[in] depth node depth
    std::string get_nodeinfo(Sint32 level);

private:
    /// reference to a primitive
    IPrimitive * m_p_prim_ref;
};
//----------------------------------------------------------------------
} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_SGPRIMITIVENODE_HH
