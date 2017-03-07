#version 400 core

in vec2 passTextureCoords;
in vec3 surfaceNormal;
in vec3 towardsLightVector;
in vec3 towardsCameraVector;

out vec4 outColor;

uniform sampler2D sampler;
uniform vec3 lightColor;
uniform float reflectivity;
uniform float shineDampness;

void main(){

	vec3 unitNormal = normalize(surfaceNormal);
	vec3 unitLightVector = normalize(towardsLightVector);
	vec3 unitCameraVector = normalize(towardsCameraVector);
	vec3 lightDirection = -unitLightVector; 
	vec3 reflectedLightDirection = reflect(lightDirection, unitNormal);

	float cost = dot(unitNormal, unitLightVector);
	float brightness = max(cost, 0.1);

	vec3 diffuse = brightness * lightColor;

	float specularFactor = dot(reflectedLightDirection, unitCameraVector);
	specularFactor = max(specularFactor, 0.0);
	float dampenedFactor = pow(specularFactor, shineDampness);
	vec3 finalSpecular = dampenedFactor * reflectivity * lightColor;

	vec4 textureColor = texture(sampler, passTextureCoords);

	if(textureColor.a < 0.5){
		discard;
	}

	outColor = vec4(((vec4(diffuse, 1.0) * textureColor) + vec4(finalSpecular, 1.0)).xyz, 0.5);
}