#version 400 core

in vec2 passTextureCoords;
in vec3 surfaceNormal;
in vec3 towardsLightVector;
in vec3 towardsCameraVector;

out vec4 outColor;

uniform sampler2D backgroundTexture;
uniform sampler2D rTexture;
uniform sampler2D gTexture;
uniform sampler2D bTexture;
uniform sampler2D blendMap;

uniform vec3 lightColor;
uniform float reflectivity;
uniform float shineDampness;

void main(){

	vec4 blendMapColor = texture(blendMap, passTextureCoords);

	float backTextureAmount = 1 - (blendMapColor.r + blendMapColor.g + blendMapColor.b);
	vec2 tiledCoords = passTextureCoords;
	vec4 backTextureColor = texture(backgroundTexture, tiledCoords) * backTextureAmount;
	vec4 rTextureColor = texture(rTexture, tiledCoords) * blendMapColor.r;
	vec4 gTextureColor = texture(gTexture, tiledCoords) * blendMapColor.g;
	vec4 bTextureColor = texture(bTexture, tiledCoords) * blendMapColor.b;

	vec4 finalColor = backTextureColor + rTextureColor + gTextureColor + bTextureColor;

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

	outColor = vec4(((vec4(diffuse, 1.0) * finalColor) + vec4(finalSpecular, 1.0)).xyz, 0.5);
}