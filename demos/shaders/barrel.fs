#version 120
//precision mediump float;
//fragcolor

uniform sampler2D tex0;
uniform vec3 unib[5];
uniform vec3 unif[20];


varying vec2 texcoordout;

// TODO: move to attribute parameter, see pi3d.Shape.set_custom_data
const float scaleFactor = 1.0;
const float DistortionXCenterOffset = -0.25 *0.0;
const float x = 0.0;
const float y = 0.0;
const float w = 0.5;
const float h = 1.0;



const float as = w/h;
const vec4 HmdWarpParam   = vec4( 1, 0.22, 0.24, 0);
const vec2 u_lensCenter   = vec2( x + (w + DistortionXCenterOffset * 0.5)*0.5, y + h*0.5);
const vec2 u_screenCenter = vec2( x + w*0.5, y + h*0.5 );
const vec2 Scale          = vec2( (w/1.0) * scaleFactor, (h/1.0) * scaleFactor * as);
const vec2 ScaleIn        = vec2( (1.0/w), (1.0/h) / as);


// Scales input texture coordinates for distortion.
vec2 HmdWarp(vec2 in01, vec2 LensCenter) {
	vec2 theta = (in01 - LensCenter) * ScaleIn; // Scales to [-1, 1]
	float rSq = theta.x * theta.x + theta.y * theta.y;
	vec2 rvector = theta * (HmdWarpParam.x + HmdWarpParam.y * rSq +
		HmdWarpParam.z * rSq * rSq +
		HmdWarpParam.w * rSq * rSq * rSq);
	return LensCenter + Scale * rvector;
}

void main() {
    vec2 tc123 = HmdWarp(texcoordout* vec2(0.5,1.0), u_lensCenter);
	if (any(bvec2(clamp(tc123,u_screenCenter-vec2(0.25,0.5), u_screenCenter+vec2(0.25,0.5)) - tc123))) {
		gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
		return;
	}
    tc123.x = 2.0 * tc123.x ;
	gl_FragColor = texture2D(tex0, tc123);
}
