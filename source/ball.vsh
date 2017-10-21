// Copyright © 2017 Galvanized Logic Inc.
// vertex shader for spinning ball effect.
// Pass on vertex, eye, and normal information for fragment shader.

layout(location=0) in vec3 in_v;  // verticies
layout(location=1) in vec3 in_n;  // vertex normals

uniform mat4  mvpm;    // Projection * ModelView
uniform mat4  mvm;     // ModelView
out     vec3  v_n;     // vertex normal
out     vec3  v_e;     // vertex eye position.
out     vec3  c_v;     // color geneated from vertex.

void main() {

    // calculate and pass on normalized view and normal directions.
    vec4 vmod = vec4(in_v, 1.0);     // vertex in model space.
    vec4 vworld = mvm * vmod;        // vertex in world space
    v_e = -vworld.xyz;               // view vector
    v_n = (mvm * vec4(in_n, 0)).xyz; // unit normal in world space.

    // use vertex and normal values to generate colors.
    c_v = normalize(in_v)/2.0+0.5;   // -1:1 to 0:1
    gl_Position = mvpm * vmod;       // pass on vertex in clip space.
}
