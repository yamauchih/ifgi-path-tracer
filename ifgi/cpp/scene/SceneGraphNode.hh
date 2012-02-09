//----------------------------------------------------------------------
// ifgi c++ implementation: scene graph node
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief scene graph node
#ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_SCENEGRAPHNODE_HH
#define IFGI_PATH_TRACER_IFGI_CPP_SCENE_SCENEGRAPHNODE_HH

#include <string>
#include <vector>

#include "cpp/base/Exception.hh"
#include "cpp/base/types.hh"

#include "BBox.hh"

namespace ifgi
{
//----------------------------------------------------------------------
// forward declaration
class IPrimitive;

//----------------------------------------------------------------------
/// Scene Graph Node. This is a base node of any scenegraph node.
///
/// The main function of this node is a group node.
///
/// This has children, but no primitive. (A primitive means a visible
/// real objetct such as TriMesh, except bounding box.);
///
/// This node has a bounding box.
class SceneGraphNode
{
public:
    /// constructor
    /// \param[in] nodename node name
    SceneGraphNode(std::string const & nodename)
        :
        m_children(),
        m_bbox(),
        m_nodename(nodename)
    {
        // empty
    }

    /// get classname
    /// \return: scnegraph node class name
    virtual std::string get_classname() const
    {
        return std::string("SceneGraphNode");
    }

    /// append child
    /// \param[in] p_child reference to a child node
    void append_child(SceneGraphNode * p_child)
    {
        if(this->is_primitive_node()){
            throw Exception("Cannot append a child to a PrimitivNode.");
        }
        m_children.push_back(p_child);
    }

    /// has children.
    /// \return True when this node has any child
    bool has_children() const
    {
        return (!m_children.empty());
    }

    /// get number of children
    /// \return the number of children
    Sint32 children_count() const
    {
        return m_children.size();
    }

    /// get child list.
    /// \return list of children.
    std::vector< SceneGraphNode * > const * peek_children() const
    {
        return &m_children;
    }

    /// set _nodename (shown in the SceneGraph viewer as Node);
    /// \param[in] nodename nodename for scenegraph visualization
    virtual void set_nodename(std::string const & nodename)
    {
        m_nodename = nodename;
    }

    /// get _nodename
    /// \return node (instance) name
    virtual std::string get_nodename() const
    {
        return m_nodename;
    }

    /// is this a primitive node?
    /// \return True when this node is a primitive node.
    virtual bool is_primitive_node() const
    {
        return false;
    }

    /// set primitive.
    ///
    /// This is an interface and need to be implemented if the node is
    /// primitive node.
    ///
    /// \param[in] prim primitive
    virtual void set_primitive(IPrimitive const & prim)
    {
        // this node can not contain primitive
        throw Exception("SceneGraphNode::set_primitive, should use PrimitiveNode.");
    }

    /// get primitive.
    ///
    /// This is an interface and need to be implemented if the node is
    /// primitive node.
    /// \return primitive, raise exception when this is not a primitive node.
    virtual IPrimitive * peek_primitive()
    {
        // this node can not contain primitive
        throw Exception("SceneGraphNode::peek_primitive, should use PrimitiveNode.");
    }

    /// get bounding box of this node
    /// \return bounding box
    BBoxScalar const & get_bbox() const
    {
        return m_bbox;
    }

    /// Does this node have a bounding box?
    /// Default is true.
    ///
    /// \return True when the node can have a bounding box. Eg.,
    /// camera does not have own bbox.
    virtual bool has_node_bbox() const
    {
        return true;
    }

    /// assign bbox value.
    /// set the bbox object. (bbox is cloned before set.);
    /// \param bbox bounding box to be assigned.
    void set_bbox(BBoxScalar const & bbox)
    {
        m_bbox = bbox;
    }

    /// print this object for debug.
    ///
    /// \param[in] level node depth level
    void print_nodeinfo(Sint32 level)
    {
        // NIN
        abort();
        // indent = "  " * level;
        // out_str = indent + "+ " + this->get_classname() + ":" + this->get_nodename() + ", ";
        // if(this->has_node_bbox()){
        //     out_str += "Bbox: ";
        //     if(this->get_bbox().has_volume()){
        //         out_str += str(this->get_bbox()) + ", ";
        //     }else{
        //         out_str += "invalid volume, ";
        //     }
        // }else{
        //     out_str += "no bbox, ";
        // }

        // out_str += str(len(this->get_children())) + " children ";
        // print out_str;
    }

private:
    /// children of this node
    std::vector< SceneGraphNode * > m_children;
    /// bounding box of this node
    BBoxScalar m_bbox;
    /// node name
    std::string m_nodename;
};

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_SCENEGRAPHNODE_HH
