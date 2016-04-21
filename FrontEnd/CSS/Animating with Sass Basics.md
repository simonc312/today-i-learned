# Animating with Sass Basics
## Adding some functionality to vanilla css 

Declaring **variables** is easy 

	$numberOfCoffees : 3; 

Doing **math** is easy 

	.thumbnail {
		width: $size / 4;
		height: $size / 4;
	} 

Use **mixins** for variable length arguments 

	@mixin animations(animationNames...){
		animation-name: animationNames;
	} 

	.superCoolEffect {
		@include animations(fireExplosion, zoomIn, rotate420);
	}

	@keyframe rotate420 {

	0% : { rotate(420deg); }

	100% : { rotate(0); }

	}

Use **mixins** for mapping arguments 

	@mixin animationProps($count : $defaultCount, $duration : $defaultDuration, $timingFunc : $defaultTiming){
		animation-iteration-count: $count; 
		animation-duration: $duration;
		animation-timing-function: $timingFunc;
	}
	# order of properties doesn't matter either;
	$amazingAnimationProperties = (duration : 123s, timingFunc : cubic-bezier(.73,0.1,0,.94), count : infinite);

	.superCoolEffectProps {
		@include animationProps($amazingAnimationProperties...);
	}

In order to perform multiple **transforms** they can't be applied to the same element because
it will override the property. Instead apply them to parent containers 

	<svg>
		<g class="rotate180">
			<path class="zoomOut" d="M504.821,456.08c-6.715,9.108-14.185,17.834-22.419,26.079" />
		</g>
	</svg>

When performing rotations by default the **transform-origin** is top left corner 0 0 so to center the origin divide width and height of svg in half. 



