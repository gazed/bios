// Copyright © 2017 Galvanized Logic Inc.
// fragment shader for spinning ball effect.
// Combine ad-hoc texture lookups with refaction.

in      vec3  v_n;    // interpolated normal
in      vec3  v_e;    // interpolated view vector.
in      vec3  c_v;    // interpolated vertex based color.
uniform sampler2D uv; // texture based on bios icon.
out     vec4  ffc;    // final fragment color.

void main() {

    // Use refraction to generate a different color.
    float refraction = 2.417; // refraction index for diamond.
    vec3 v_r = refract(normalize(v_e), normalize(v_n), 1.0 / refraction);
    vec4 c1 = texture(uv, ((v_r/2.0)+0.5).xz);

    // Generate colors based on vertex to get subsurface look.
    vec4 c2 = texture(uv, c_v.yz);
    vec4 c3 = texture(uv, c_v.xy);

    // combine the colors.
    ffc =  mix(c1*1.5 , c2+c3, 0.5);
}
