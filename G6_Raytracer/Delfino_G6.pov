#include "colors.inc"
#include "textures.inc"
#include "finish.inc"
#include "skies.inc"
#include "woods.inc"
#include "glass.inc"
#include "metals.inc"
global_settings {assumed_gamma 1.0}

// The custom Surface of Rotation object is the cup on the table, generated using the unit circle

#declare PictureFrame = /* Planar image map */
texture {pigment{image_map { jpeg "frame.jpg" map_type 0 once interpolate 2 } } }

#declare WindowGlass =
texture{
  pigment{ rgbf<0.98,0.98,0.98,0.85>} // 0.85
  finish { diffuse 0.1
           reflection 0.2
           specular 0.8
           roughness 0.0003
           phong 1
           phong_size 400}
  } // end of texture --------------

#declare TABLE = texture {
    finish { Shiny }
    pigment{Brown}
    }

#include "tree.inc"
#include "table.inc"
#include "window.inc"
#include "chair.inc"
#include "grass.inc"
#include "grass2.inc"
#include "grass3.inc"
#include "customSurface.inc"
camera {
    location <-2, 3, -12>
    look_at  <1, 0,  0>//z = 1,0,0
  }

light_source {
	< -25, 23, 35>
	rgb <1.0, 1.0, 1.0> * 1.0
}

// light_source {
//   < 2, 3, -0>
//   rgb <0.85, 0.6, 0.0> * 0.3
// }

plane { <0, 1, 0>, -17
    texture {
      T_Chrome_2D
      normal {
         waves 0.05
         frequency 5000.0
         scale 3000.0
      }
   }
}

box {       // wall to the right of window
    <4, -4, -20>,
    <58, -4, 12.5>
    scale <2,1,1>
    texture { T_Wood18 finish{Shiny}}
    // rotate < 93, 0, 0 >
    // rotate < 0, -32, 0 >
    // translate < -3.28,0,5.38>
    rotate < 85, 0, 0 >
    rotate < 0, -32, 0 >
    translate < -3.75,0,6.15>
}

box {       // wall below window
    <-10, -4, 3>,
    <15, -4, 12.5>
    scale <2,1,1>
    texture { T_Wood18 finish{Shiny}}
    rotate < 85, 0, 0 >
    rotate < 0, -32, 0 >
    translate < -3.75,0,6.15>
}

box {       // ceiling
    <-10, -4, -9>,
    <58, -30, -8.5>
    scale <2,1,1>
    texture { pigment{White} finish{Shiny}}
    rotate < 85, 0, 0 >
    rotate < 35, 0, 0>
    rotate < 0, -32, 0 >
    translate < -4.25,0,7>
}

box {       // floor
    <-10, -4, 12>,
    <58, -30, 12.5>
    scale <2,1,1>
    texture { T_Wood11 finish{Shiny}}
    rotate < 85, 0, 0 >
    rotate < 0, -32, 0 >
    translate < -3.75,0,6.15>
}
sky_sphere{ pigment { image_map{jpeg "mounts.jpg"} scale y*0.23 rotate <0,-25,0>}}


// picture frame
plane {
   z, 0
   hollow on
   clipped_by {box { <0, 0, -1>, <1, 1, 1> } }
   texture { PictureFrame }
   translate <-0.5, -0.5, 0>
   scale 7
   translate <23, 5.5, 3.75>

   // rotate <0, 0, 4>
   rotate <5, 0, 0>
   rotate <0, -26, 0>

}

// glass window pane
plane {
   z, 0
   hollow on
   clipped_by {box { <0, 0, -1>, <1, 1, 1> } }
   texture { WindowGlass }
   translate <-0.5, -0.5, 0>
   scale <28, 7.75, 1>
   translate <-4.1, 0, 3.32>

   // rotate <0, 0, 4>
   rotate <2, 0, 0>
   rotate <0, -29, 0>

}
