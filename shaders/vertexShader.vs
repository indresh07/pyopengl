#version 400 core

in vec3 position;
in vec2 textureCoords;
in vec3 normal;

out vec2 passTextureCoords;
out vec3 towardsLightVector;
out vec3 surfaceNormal;
out vec3 towardsCameraVector;

uniform mat4 transformationMatrix;
uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;
uniform vec3 lightPosition;
uniform float fakeLight;

void main(){
			
	vec4 worldPosition = vec4(position, 1.0) * transformationMatrix;
	gl_Position = (projectionMatrix * (worldPosition * viewMatrix));
	passTextureCoords = textureCoords;
	vec3 actualNormal = normal;
	if(fakeLight == 1){
		actualNormal = vec3(0.0, 1.0, 0.0);	
	}
	surfaceNormal = (vec4(actualNormal, 0.0) * transformationMatrix).xyz;
	towardsLightVector = lightPosition - worldPosition.xyz;
	towardsCameraVector = -(inverse(viewMatrix) * vec4(0.0, 0.0, 0.0, 1.0)).xyz + worldPosition.xyz;
}