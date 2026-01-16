## Lista 8: GLSL Shaders and Ray Marching

GPU-accelerated 3D rendering using GLSL shaders and ray marching techniques on ShaderToy platform.

## Overview

This project explores real-time 3D graphics using:
- **Signed Distance Fields (SDFs)**: Mathematical representation of 3D shapes
- **Ray Marching**: Rendering technique for implicit surfaces
- **GLSL**: OpenGL Shading Language for GPU programming

**Platform**: ShaderToy (https://www.shadertoy.com/)

## What Was Improved

### Original Implementation
- ✅ Working GLSL shaders on ShaderToy
- ✅ Ray marching implementation
- ✅ 3D transformations and deformations

### Documentation Improvements
- ✅ **Comprehensive README**: Theory and technique explanations
- ✅ **Code comments**: Inline documentation
- ✅ **Portability guide**: How to use shaders outside ShaderToy
- ✅ **Learning resources**: Tutorials and references

## Theory

### Signed Distance Functions (SDFs)

Mathematical functions that return distance to nearest surface:

```glsl
// Sphere SDF
float sdSphere(vec3 p, float radius) {
    return length(p) - radius;
}

// Box SDF
float sdBox(vec3 p, vec3 b) {
    vec3 d = abs(p) - b;
    return min(max(d.x, max(d.y, d.z)), 0.0) + length(max(d, 0.0));
}
```

**Properties**:
- Negative inside object
- Zero at surface
- Positive outside object
- Magnitude = distance to surface

### Ray Marching Algorithm

```glsl
float march(vec3 ro, vec3 rd) {
    float t = 0.0;
    for(int i = 0; i < MAX_STEPS; i++) {
        vec3 p = ro + rd * t;
        float d = sceneSDF(p);

        if(d < EPSILON) return t;  // Hit!
        if(t > MAX_DIST) break;    // Too far

        t += d;  // March by distance
    }
    return -1.0;  // Miss
}
```

**Why efficient?**
- SDF tells safe distance to march
- Large steps when far from surfaces
- Small steps near surfaces
- Typically converges in <100 steps

### Advantages over Triangle Rasterization

**Pros**:
- Infinite detail (resolution independent)
- Easy boolean operations (union, intersection, subtraction)
- Smooth blending
- Exact ray-surface intersection

**Cons**:
- Limited to implicit surfaces
- Can be slow for complex scenes
- Less hardware support than triangle rasterization

## ShaderToy Platform

### Features
- **Web-based**: No installation required
- **Live coding**: Real-time preview
- **Community**: Share and remix shaders
- **Built-in uniforms**: Mouse, time, resolution

### Key Uniforms

```glsl
uniform vec3 iResolution;  // Viewport resolution (pixels)
uniform float iTime;       // Shader playback time (seconds)
uniform vec4 iMouse;       // Mouse pixel coords (xy: current, zw: click)
uniform int iFrame;        // Shader playback frame
```

## Viewing the Shaders

### On ShaderToy

1. Visit https://www.shadertoy.com/
2. Click "New"
3. Paste shader code
4. Click "Compile & Run"

### Local Viewing (Advanced)

Convert to standalone WebGL:

```html
<!DOCTYPE html>
<html>
<body>
<canvas id="canvas"></canvas>
<script>
    const canvas = document.getElementById('canvas');
    const gl = canvas.getContext('webgl');

    // Vertex shader
    const vsSource = `
        attribute vec2 position;
        void main() {
            gl_Position = vec4(position, 0.0, 1.0);
        }
    `;

    // Fragment shader (paste ShaderToy code here)
    const fsSource = `
        precision highp float;
        uniform vec2 iResolution;
        uniform float iTime;

        // ... your shader code ...

        void main() {
            mainImage(gl_FragColor, gl_FragCoord.xy);
        }
    `;

    // Compile and link program
    // ... WebGL boilerplate ...
</script>
</body>
</html>
```

## Key Techniques

### 1. Transformations

```glsl
// Translation
vec3 translate(vec3 p, vec3 offset) {
    return p - offset;
}

// Rotation (around Y axis)
vec3 rotateY(vec3 p, float angle) {
    float c = cos(angle);
    float s = sin(angle);
    mat3 m = mat3(c, 0, s, 0, 1, 0, -s, 0, c);
    return m * p;
}

// Scale
vec3 scale(vec3 p, float s) {
    return p / s;
}
```

### 2. Boolean Operations

```glsl
// Union (OR)
float opUnion(float d1, float d2) {
    return min(d1, d2);
}

// Subtraction
float opSubtraction(float d1, float d2) {
    return max(-d1, d2);
}

// Intersection (AND)
float opIntersection(float d1, float d2) {
    return max(d1, d2);
}

// Smooth Union (blend)
float opSmoothUnion(float d1, float d2, float k) {
    float h = clamp(0.5 + 0.5*(d2-d1)/k, 0.0, 1.0);
    return mix(d2, d1, h) - k*h*(1.0-h);
}
```

### 3. Lighting

```glsl
vec3 calcNormal(vec3 p) {
    vec2 e = vec2(0.001, 0.0);
    return normalize(vec3(
        sceneSDF(p + e.xyy) - sceneSDF(p - e.xyy),
        sceneSDF(p + e.yxy) - sceneSDF(p - e.yxy),
        sceneSDF(p + e.yyx) - sceneSDF(p - e.yyx)
    ));
}

vec3 phong(vec3 p, vec3 rd, vec3 lightPos) {
    vec3 N = calcNormal(p);
    vec3 L = normalize(lightPos - p);
    vec3 R = reflect(-L, N);

    float diffuse = max(dot(N, L), 0.0);
    float specular = pow(max(dot(R, -rd), 0.0), 32.0);

    return vec3(0.1) + diffuse * vec3(0.7) + specular * vec3(0.3);
}
```

## Applications

1. **Real-time Graphics**: Games, demos, visualizations
2. **Mathematical Visualization**: Fractals, implicit surfaces
3. **Art**: Generative art, music videos
4. **Education**: Teaching 3D math and rendering
5. **Prototyping**: Quick 3D concept visualization

## Learning Resources

### Tutorials
- **Inigo Quilez**: https://iquilezles.org/articles/ (SDF pioneer)
- **ShaderToy Tutorial**: https://inspirnathan.com/posts/47-shadertoy-tutorial-part-1/
- **Ray Marching**: https://michaelwalczyk.com/blog-ray-marching.html

### Examples
- **ShaderToy Featured**: https://www.shadertoy.com/ (Browse)
- **The Book of Shaders**: https://thebookofshaders.com/

### SDF Library
- **HG_SDF**: https://mercury.sexy/hg_sdf/ (Comprehensive SDF collection)

## Common SDFs

```glsl
// Primitives
float sdSphere(vec3 p, float r);
float sdBox(vec3 p, vec3 b);
float sdCylinder(vec3 p, float h, float r);
float sdTorus(vec3 p, vec2 t);
float sdCapsule(vec3 p, vec3 a, vec3 b, float r);

// Complex
float sdOctahedron(vec3 p, float s);
float sdMandelbulb(vec3 p);  // 3D Mandelbrot fractal
```

## Performance Tips

1. **Minimize SDF evaluations**: Expensive in loops
2. **Use bounding volumes**: Skip complex shapes when far away
3. **Reduce MAX_STEPS**: Trade quality for speed
4. **Optimize math**: Use fast approximations
5. **Cache results**: Avoid recalculating normals

## Porting to Other Platforms

### Three.js (JavaScript)
```javascript
const fragmentShader = `
    // Paste GLSL code here
`;

const material = new THREE.ShaderMaterial({
    fragmentShader: fragmentShader,
    uniforms: {
        iTime: { value: 0 },
        iResolution: { value: new THREE.Vector2() }
    }
});
```

### Unity (C# + HLSL)
```csharp
Shader "Custom/RayMarching" {
    SubShader {
        Pass {
            CGPROGRAM
            #pragma fragment frag
            // Translate GLSL to HLSL
            ENDCG
        }
    }
}
```

## References

1. **Hart, J. C.** (1996). "Sphere tracing: A geometric method for the antialiased ray tracing of implicit surfaces". *The Visual Computer*, 12(10), 527-545.
2. **Quilez, I.** (2008-present). "Rendering Worlds with Two Triangles". https://iquilezles.org/
3. **Pharr, M., Jakob, W., & Humphreys, G.** (2016). *Physically Based Rendering*. Morgan Kaufmann.

## Project Structure

```
Lista8_shader/
├── shader1.glsl        # Main shader code
├── shader2.glsl        # Variations
├── Sprawozdanie.md     # Project report (Polish)
└── README.md           # This file
```

---

**Note**: ShaderToy shaders are self-contained and run in browser. No local compilation needed. This project demonstrates advanced GPU programming and mathematical visualization techniques.

**Author**: Mateusz Wojteczek
**Platform**: ShaderToy / GLSL
**Course**: Modelowanie Komputerowe
