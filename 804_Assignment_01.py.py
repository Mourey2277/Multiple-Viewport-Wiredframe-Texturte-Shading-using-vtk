# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 11:29:00 2019

@author: Jannatul Mourey 

"""
import vtk

pole = [1., 12., 3.]

#Reading the Apple objecr from file
reader = vtk.vtkOBJReader()
reader.SetFileName('apple_obj.obj')
reader.Update()

#Reading the Apple texture from file
reader2= vtk.vtkJPEGReader()
reader2.SetFileName('apple_texture.jpg')
reader2.Update()

texture = vtk.vtkTexture()
texture.SetInputConnection(reader2.GetOutputPort())
texture.InterpolateOn()

#Creating Mapper for Wireframed Apple
appleMapper1= vtk.vtkPolyDataMapper()
appleMapper1.SetInputConnection(reader.GetOutputPort())
appleMapper1.SetResolveCoincidentTopologyPolygonOffsetParameters(1, 1)
appleMapper1.SetResolveCoincidentTopologyToPolygonOffset()

#Creating Actor for Wireframed Apple
appleActor1= vtk.vtkActor()
appleActor1.SetMapper(appleMapper1)
appleActor1.GetProperty().SetColor(1,1,1)
appleActor1.GetProperty().SetRepresentationToWireframe()
appleActor1.SetOrigin(pole)
appleActor1.RotateX(90.)

#Creating Mapper for Normal White Apple 
appleMapper2 = vtk.vtkPolyDataMapper()
appleMapper2.SetInputConnection(reader.GetOutputPort())

#Creating Actor for Normal White Apple 
appleActor2 = vtk.vtkActor()
appleActor2.SetMapper(appleMapper2)
appleActor2.GetProperty().SetColor(1,1,1) #Setting White color on it's surface
appleActor2.RotateX(90.) # Rotating 90 degree 

#Creating Mapper for Texture Apple 
appleMapper3 = vtk.vtkPolyDataMapper()
appleMapper3.SetInputConnection(reader.GetOutputPort())

#Creating Actor for Texture Apple 
appleActor3 = vtk.vtkActor()
appleActor3.SetMapper(appleMapper3)
appleActor3.SetTexture(texture) #Setting texture or it's surface
appleActor3.RotateX(90.)# Rotating 90 degree 

#Creating Mapper for Shaded Apple 
appleMapper4 = vtk.vtkPolyDataMapper()
appleMapper4.SetInputConnection(reader.GetOutputPort())

#Creating Actor for Shaded Apple
appleActor4 = vtk.vtkActor()
appleActor4.SetMapper(appleMapper4)
appleActor4.SetTexture(texture)#Setting texture or it's surface
appleActor4.RotateX(90.)# Rotating 90 degree 

# Compute normals for the Shaded Apple
normals = vtk.vtkPolyDataNormals()
normals.SetInputConnection(reader.GetOutputPort())

# VTK pipeline for Shaded Apple mapper and actor
appleMapper4.SetInputConnection(normals.GetOutputPort())
appleActor4.SetMapper(appleMapper4)

# Set object properties
prop = appleActor4.GetProperty()
prop.SetInterpolationToPhong() # Set shading to Phong
prop.ShadingOn()
prop.SetColor(1, 1, 0)
prop.SetDiffuse(0.8) # 0.8
prop.SetAmbient(0.1) # 0.3
prop.SetSpecular(0.5) # 1.0
prop.SetSpecularPower(100.0)

# Define light for the shaded Apple 
light = vtk.vtkLight ()
light.SetLightTypeToSceneLight()
light.SetAmbientColor(.5, .5, .5)
light.SetDiffuseColor(.5, .5,.5)
light.SetSpecularColor(1,1,1)
light.SetPosition(-100, 100, 25)
light.SetFocalPoint(0,0,0)
light.SetIntensity(1.0)

# Add the Wireframed Apple Actor to the renderer
ren1 = vtk.vtkRenderer()
ren1.SetViewport(0, 0.5, 0.5, 1)#Setting the View Port
ren1.SetBackground(0.5, 0.5, 0.5)#Setting the background
ren1.AddActor(appleActor1)


# Add the Normal Apple Actor to the renderer
ren2 = vtk.vtkRenderer()
ren2.SetViewport(0, 0, 0.5, 0.5)#Setting the View Port
ren2.SetBackground(0.5, 0.5, 0.5)#Setting the background
ren2.AddActor(appleActor2)

# Add the Textured Apple Actor to the renderer
ren3 = vtk.vtkRenderer()
ren3.SetViewport(0.5, 0.5, 1, 1)#Setting the View Port
ren3.SetBackground(0.5, 0.5, 0.5)#Setting the background
ren3.AddActor(appleActor3)

# Add the Shaded Apple Actor to the renderer
ren4 = vtk.vtkRenderer()
ren4.SetViewport(0.5, 0, 1, 0.5)#Setting the View Port
ren4.AddLight(light)# Add the light to the renderer
ren4.SetBackground(0.5, 0.5, 0.5)#Setting the background
ren4.AddActor(appleActor4)

#Creating the Render window and defining it's size 
renWin = vtk.vtkRenderWindow()
renWin.SetSize(600, 300)

#Render the scenes
renWin.AddRenderer(ren1)
renWin.AddRenderer(ren2)
renWin.AddRenderer(ren3)
renWin.AddRenderer(ren4)
renWin.Render()

# Creating ender window interactor to captures mouse events and perform 
#appropriate camera or actor manipulation depending on the nature of the events
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

#Getting screenshot of the output window
windowToImageFilter = vtk.vtkWindowToImageFilter()
windowToImageFilter.SetInput(renWin)
windowToImageFilter.Update()
 
writer = vtk.vtkJPEGWriter()
writer.SetFileName("Output_of_Code.jpeg")

#writer.SetWriteToMemory(1)
writer.SetInputConnection(windowToImageFilter.GetOutputPort())
writer.Write()

iren.Initialize()# Initalizing the interactor for the loop 
iren.Start() # Start the event loop


