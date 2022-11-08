from OCC.Display.SimpleGui import *     #init_display
from OCC.Core.BRepPrimAPI import *      #BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere
from OCC.Core.gp import *               #gp_Pnt
import OCC.Core.BRepAlgoAPI
from OCC.Core.BRepBuilderAPI import *
from OCC.Core.GC import *
from OCC.Core.TopoDS import *
import numpy
import sys
import math
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.Geom import Geom_BezierCurve
from OCC.Core.STEPControl import *
from OCC.Core.BRepOffsetAPI import *
from OCC.Core.Precision import *
from OCC.Core.TopExp import *
from OCC.Core.TopAbs import *
from OCC.Core.TopoDS import *
from OCC.Core.BRep import *
from OCC.Core.gp import gp_Dir, gp_Pln, gp_Ax3, gp_XOY
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_DraftAngle
from OCC.Core.Precision import precision_Angular
from OCC.Core.BRep import BRep_Tool_Surface
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.Geom import Geom_Plane
from OCC.Core.TopoDS import topods_Face



def exit(event=None):
    sys.exit()


def draw_nothing(event=None):
    pass


def draw_box(event=None):
    erase_all()
    my_box_shape = BRepPrimAPI_MakeBox(10., 20., 30.).Shape()
    display.DisplayShape(my_box_shape, update=True)
    step_writer.Transfer(my_box_shape, STEPControl_AsIs)


def draw_sphere(event=None):
    erase_all()
    radius = 50.0
    x = 0.0
    y = 0.0
    z = 0.0

    point = gp_Pnt(x, y, z)
    my_sphere = BRepPrimAPI_MakeSphere(point, radius).Shape()
    display.DisplayShape(my_sphere, update=True)
    step_writer.Transfer(my_sphere, STEPControl_AsIs)


def erase_all(event=None):
    display.EraseAll()


def draw_red_sphere(event=None):
    erase_all()
    radius = 50.0
    x = 0.0
    y = 1.0
    z = 1.414

    point = gp_Pnt(x, y, z)
    my_sphere = BRepPrimAPI_MakeSphere(point, radius).Shape()
    display.DisplayColoredShape(my_sphere, color='RED', update=True)


def sphere_from_vector_and_radius(vector, radius):
    x = float(vector[0][0])
    y = float(vector[1][0])
    z = float(vector[2][0])
    point = gp_Pnt(x, y, z)
    sphere = BRepPrimAPI_MakeSphere(point, radius)
    return sphere


def draw_sphere_1(event=None):
    Radius = 50.0
    PointZeroArray = numpy.zeros((3, 1), dtype=float)
    MySphereShape = sphere_from_vector_and_radius(PointZeroArray, Radius).Shape()
    display.DisplayColoredShape(MySphereShape, 'RED', update=True)


def draw_sphere_2(event=None):
    Radius = 50.0
    MyPointAsArray = numpy.array([25.0, 50.0, 50.0])
    MyPointAsArray = numpy.reshape(MyPointAsArray, (3, 1))
    MySphereShape = sphere_from_vector_and_radius(MyPointAsArray, Radius).Shape()
    display.DisplayColoredShape(MySphereShape, 'YELLOW', update=True)


def draw_common_spheres(event=None):
    erase_all()
    Radius = 50.0
    PointZeroArray = numpy.zeros((3,1), dtype=float)
    MySphereShape1 = sphere_from_vector_and_radius(PointZeroArray, Radius).Shape()

    Radius = 50.0
    MyPointAsArray = numpy.array([25.0, 50.0, 50.0])
    MyPointAsArray = numpy.reshape(MyPointAsArray, (3,1))
    MySphereShape2 = sphere_from_vector_and_radius(MyPointAsArray, Radius).Shape()
    CuttedSpheres = OCC.Core.BRepAlgoAPI.BRepAlgoAPI_Common(MySphereShape1, MySphereShape2).Shape()
    display.DisplayColoredShape(CuttedSpheres, 'BLUE', update=True)


def draw_cutted_spheres(event=None):
    erase_all()
    Radius = 50.0
    PointZeroArray = numpy.zeros((3, 1), dtype=float)
    MySphereShape1 = sphere_from_vector_and_radius(PointZeroArray, Radius).Shape()

    Radius = 50.0
    MyPointAsArray = numpy.array([25.0, 50.0, 50.0])
    MyPointAsArray = numpy.reshape(MyPointAsArray, (3, 1))
    MySphereShape2 = sphere_from_vector_and_radius(MyPointAsArray, Radius).Shape()
    CuttedSpheres = OCC.Core.BRepAlgoAPI.BRepAlgoAPI_Cut(MySphereShape2, MySphereShape1).Shape()
    display.DisplayColoredShape(CuttedSpheres, 'BLUE', update=True)


def draw_fused_spheres(event=None):
    erase_all()
    Radius = 50.0
    PointZeroArray = numpy.zeros((3,1), dtype=float)
    MySphereShape1 = sphere_from_vector_and_radius(PointZeroArray, Radius).Shape()

    MyPointAsArray = numpy.array([25.0, 50.0, 50.0])
    MyPointAsArray = numpy.reshape(MyPointAsArray, (3, 1))
    MySphereShape2 = sphere_from_vector_and_radius(MyPointAsArray, Radius).Shape()
    FusedShperes = OCC.Core.BRepAlgoAPI.BRepAlgoAPI_Fuse(MySphereShape2, MySphereShape1).Shape()
    display.DisplayColoredShape(FusedShperes, 'BLUE', update=True)


def draw_cube_with_wire_model(event=None):
    # Vertices of one face of cube
    aPnt1 = gp_Pnt(0, 0, 0)
    aPnt2 = gp_Pnt(10, 0, 0)
    aPnt3 = gp_Pnt(10, 10, 0)
    aPnt4 = gp_Pnt(0, 10, 0)

    # Join the vertices to make an edge directly with points. Can also use segment(See document)
    aEdge1 = BRepBuilderAPI_MakeEdge(aPnt1, aPnt2)
    aEdge2 = BRepBuilderAPI_MakeEdge(aPnt2, aPnt3)
    aEdge3 = BRepBuilderAPI_MakeEdge(aPnt3, aPnt4)
    aEdge4 = BRepBuilderAPI_MakeEdge(aPnt4, aPnt1)

    # Connect the edges to make a wire frame
    aWire = BRepBuilderAPI_MakeWire(aEdge1.Edge(), aEdge2.Edge(), aEdge3.Edge(), aEdge4.Edge())

    # Make a surface from wire frame (Like dipping frame in soap solution)
    myFaceProfile = BRepBuilderAPI_MakeFace(aWire.Wire())

    # A vector in the direction of height(Till now we have a 2d sheet only
    aPrismVec = gp_Vec(0, 0, 20)

    # Square to Block conversion
    myBody = BRepPrimAPI_MakePrism(myFaceProfile.Face(), aPrismVec)

    # Can also display face, wire, edge, pnt individually by shape_type.Shape()
    display.DisplayShape(myBody.Shape(), update=True)


def draw_mirror(event=None):
    myWidth = 40.0
    myThickness = 80.0
    myHeight = 20.0

    aPnt1 = gp_Pnt(-myWidth/2., 0, 0)
    aPnt2 = gp_Pnt(-myWidth/2., -myThickness/4., 0)
    aPnt3 = gp_Pnt(0, -myThickness/2., 0)
    aPnt4 = gp_Pnt(myWidth/2., -myThickness/4., 0)
    aPnt5 = gp_Pnt(myWidth/2., 0 , 0)

    aArcOfCircle = GC_MakeArcOfCircle(aPnt2, aPnt3, aPnt4)
    aSegment1 = GC_MakeSegment(aPnt1, aPnt2)
    aSegment2 = GC_MakeSegment(aPnt4, aPnt5)

    aEdge1 = BRepBuilderAPI_MakeEdge(aSegment1.Value())
    aEdge2 = BRepBuilderAPI_MakeEdge(aArcOfCircle.Value())
    aEdge3 = BRepBuilderAPI_MakeEdge(aSegment2.Value())

    aWire = BRepBuilderAPI_MakeWire(aEdge1.Edge(), aEdge2.Edge(), aEdge3.Edge())

    # Make Mirror
    xAxis = gp_OX()
    aTrsf = gp_Trsf()
    aTrsf.SetMirror(xAxis)
    aBRepTrsf = BRepBuilderAPI_Transform(aWire.Shape(), aTrsf)
    aMirroredShape = aBRepTrsf.Shape()
    aMirroredWire = topods_Wire(aMirroredShape)
    mkWire = BRepBuilderAPI_MakeWire()
    mkWire.Add(aWire.Wire())
    
    # Add Mirror to Wire
    mkWire.Add(aMirroredWire)
    
    myWireProfile = mkWire.Wire()

    # Body
    myFaceProfile = BRepBuilderAPI_MakeFace(myWireProfile)
    aPrismVec = gp_Vec(0, 0, myHeight)
    myBody = BRepPrimAPI_MakePrism(myFaceProfile.Face(), aPrismVec)
    display.DisplayShape(myBody.Shape(), update=True)


def draw_edge(event=None):
    # Blue Edge - From gp_Pnt
    BlueEdge = BRepBuilderAPI_MakeEdge(gp_Pnt(-80, -50, -20), gp_Pnt(-30, -60, -60))

    # Yellow Edge - From Vertices
    V1 = BRepBuilderAPI_MakeVertex(gp_Pnt(-20, 10, -30))
    V2 = BRepBuilderAPI_MakeVertex(gp_Pnt(10, 7, -25))
    YellowEdge = BRepBuilderAPI_MakeEdge(V1.Vertex(), V2.Vertex())

    # White Edge - see OCC docs on gp_Lin(gp_Ax1), creates a line along the reference axis gp_Ax1
    line = gp_Lin(gp_Ax1(gp_Pnt(10, 10, 10), gp_Dir(1, 0, 0)))  # Axis passes thr gp_Pnt and parallel to gp_Dir vector
    WhiteEdge = BRepBuilderAPI_MakeEdge(line, -20, 10)

    # White Edge- A portion of ellipse
    Ellipse = gp_Elips(gp_Ax2(gp_Pnt(10, 0, 0), gp_Dir(1, 1, 1)), 60, 30)  # See gp_Ax2 docs. Major Ax=60, Minor=30
    RedEdge = BRepBuilderAPI_MakeEdge(Ellipse, 0, math.pi / 2) # Args are angles 0 to pi/2 with reference X axis

    # Green Edge - Bezier curve with points 1 to 8 in order
    P1 = gp_Pnt(-15, 200, 10)
    P2 = gp_Pnt(5, 204, 0)
    P3 = gp_Pnt(15, 200, 0)
    P4 = gp_Pnt(-15, 20, 15)
    P5 = gp_Pnt(-5, 20, 0)
    P6 = gp_Pnt(15, 20, 0)
    P7 = gp_Pnt(24, 120, 0)
    P8 = gp_Pnt(-24, 120, 12.5)

    array = TColgp_Array1OfPnt(1, 8)  # Array of points
    array.SetValue(1, P1)
    array.SetValue(2, P2)
    array.SetValue(3, P3)
    array.SetValue(4, P4)
    array.SetValue(5, P5)
    array.SetValue(6, P6)
    array.SetValue(7, P7)
    array.SetValue(8, P8)

    curve = Geom_BezierCurve(array)
    ME = BRepBuilderAPI_MakeEdge(curve)
    GreenEdge = ME
    V3 = ME.Vertex1()
    V4 = ME.Vertex2()

    display.DisplayColoredShape(BlueEdge.Edge(), 'BLUE')
    display.DisplayShape(V1.Vertex())
    display.DisplayShape(V2.Vertex())
    display.DisplayColoredShape(WhiteEdge.Edge(), 'WHITE')
    display.DisplayColoredShape(YellowEdge.Edge(), 'YELLOW')
    display.DisplayColoredShape(RedEdge.Edge(), 'RED')
    display.DisplayColoredShape(GreenEdge.Edge(), 'GREEN')
    display.DisplayShape(V3)
    display.DisplayShape(V4, update=True)


def draft_angle(event=None):
    S = BRepPrimAPI_MakeBox(200., 300., 150.).Shape()
    adraft = BRepOffsetAPI_DraftAngle(S)
    topExp = TopExp_Explorer()
    topExp.Init(S, TopAbs_FACE)
    while topExp.More():
        face = topods_Face(topExp.Current())
        surf = Geom_Plane.DownCast(BRep_Tool_Surface(face))
        dirf = surf.Pln().Axis().Direction()
        ddd = gp_Dir(0, 0, 1)
        if dirf.IsNormal(ddd, precision_Angular()):
            adraft.Add(face, ddd, math.radians(15), gp_Pln(gp_Ax3(gp_XOY())))
        topExp.Next()
    adraft.Build()
    display.DisplayShape(adraft.Shape(), update=True)


def export_stl():
    pass


def export_step():  # Only exports my_box_shape for now(17/05/22). Will be included in all functions later
    step_writer.Write("step_file.stp")


display, start_display, add_menu, add_function_to_menu = init_display()
step_writer = STEPControl_Writer()

add_menu('File')

add_function_to_menu('File', erase_all)
add_function_to_menu('File', exit)

add_menu('Draw')

add_function_to_menu('Draw', draw_nothing)
add_function_to_menu('Draw', draw_box)
add_function_to_menu('Draw', draw_sphere)
add_function_to_menu('Draw', draw_sphere_1)
add_function_to_menu('Draw', draw_sphere_2)
add_function_to_menu('Draw', draw_red_sphere)
add_function_to_menu('Draw', draw_cube_with_wire_model)
add_function_to_menu('Draw', draw_mirror)
add_function_to_menu('Draw', draw_edge)
add_function_to_menu('Draw', draft_angle)

add_menu('Boolean')

add_function_to_menu('Boolean', draw_common_spheres)
add_function_to_menu('Boolean', draw_cutted_spheres)
add_function_to_menu('Boolean', draw_fused_spheres)

add_menu('Export')

add_function_to_menu('Export', export_stl)
add_function_to_menu('Export', export_step)

start_display()
