//----------------------------------------------------------------------
// ifgi c++ implementation: SGMaterialNode.hh
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief scene graph material node
#ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_SGMATERIALNODE_HH
#define IFGI_PATH_TRACER_IFGI_CPP_SCENE_SGMATERIALNODE_HH

#include "SceneGraphNode.hh"

#include "cpp/base/ILog.hh"

namespace ifgi
{
//----------------------------------------------------------------------
// forward declaration
class IMaterial;

//----------------------------------------------------------------------
/// Material node. a Scene Graph Node.
///
/// Material node for ifgi is attached under the material group
/// under the scenegraph root.
class SGMaterialNode : public SceneGraphNode
{
public:
    /// constructor
    /// \param[in] nodename node name
    SGMaterialNode(std::string const & nodename);

    /// get classname
    /// \return scnegraph node class name
    virtual std::string get_classname() const;

    /// is this a primitive node?
    /// \return False. material can not visualize without primitive.
    virtual bool is_primitive_node() const;

    /// get bounding box of this node
    /// This should not be called.
    /// \return invalid bbox
    // virtual BBox32 const & get_bbox() const; DELETME

    /// Does this node have a bounding box?
    /// \return False, material has no bounding box
    virtual bool has_node_bbox() const;

public:
    /// set a material.
    ///
    /// \param[in] p_mat a reference to a material
    void set_material(IMaterial * p_mat);

    /// peek the material.
    /// \return reference to the assigned material.
    IMaterial * peek_material() const;

private:
    /// reference to the material
    IMaterial * m_p_material;
};

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_SGMATERIALNODE_HH
