---
title: "User Input & Media Exports"
description: "An overview of handling user input, listening to key presses, exporting the artwork at different resolutions and passing in values as URL parameters."
source: https://docs.fxhash.xyz/creating-on-fxhash/genart-in-the-browser/user-input-and-media-exports
archived: https://web.archive.org/web/20260312073909/https://docs.fxhash.xyz/creating-on-fxhash/genart-in-the-browser/user-input-and-media-exports
captured: 2026-03-12
---
# User Input & Media Exports

*An overview of handling user input, listening to key presses, exporting the artwork at different resolutions and passing in values as URL parameters.*

Artists often choose to add additional user interaction options to their generative artworks, for instance the option to export the artwork in various formats by means of a key press, the ability to switch between different resolutions, toggling on a debug mode, as well as all kinds of other experimental user interactions. These are often nice features to have and can greatly elevate the project.

In this section we will discuss some of the methods for exporting the canvas as an image via a key press as well as other interaction options.

### Exporting the Canvas

Although the canvas can be saved as an image through the right click menu in the browser, it's a good idea to add in a dedicated key for that purpose. Just like we previously resized the canvas with an event listener, we can also use event listeners to detect key presses:

```js
// Listen for a key press event
document.addEventListener('keydown', function(event) {
  // Check if the pressed key is the 'e' key (you can change this to any key you want)
  if (event.key === 's') {
	// Call the function to export the canvas as a PNG image
	exportCanvasAsPNG(canvas);
  }
});
```

Exporting a canvas element as an image file (PNG/JPEG) can be done with the following piece of code:

```js
function exportCanvasAsPNG(canvas) {
  // Create an "a" element to trigger the download
  const link = document.createElement('a');

  // Convert the canvas to a data URL
  const dataURL = canvas.toDataURL('image/png');

  // Set the href attribute of the "a" element to the data URL
  link.href = dataURL;

  // Set the download attribute to specify the file name
  link.download = 'canvas-export.png';

  // Simulate a click on the "a" element to trigger the download
  link.click();
}
```

The canvas API provides a [function called `toDataURL()` that converts it canvas bitmap to an image file](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement).

Downloading this image involves temporarily creating a link to which it gets attached, and then simulating a click that triggers this link. We often tie this event to the s key (s as in *saving*) on our keyboard:

> **CodePen demo:** <https://codepen.io/gorillasu/pen/GRzEZOO>

P5 makes this is as straightforward as using the inbuilt `keyPressed()` and `save()` functions:

```jsx
function keyPressed() {
	// keyCodes map to specific keys on the keyboard
	// 83 maps to the 's' key
	if (keyCode === 83) {
	  // the save function exports the canvas as a PNG file
	  save();
	}
}
```

[You can find more information about this function in the P5 reference](https://p5js.org/reference/#/p5/keyPressed).

### Different Resolution Export

Sometimes we want to provide this exported image at different resolutions, this is useful if collectors want to make their own prints of the artwork or use it as a wallpaper for their devices. For this purpose we need to build a way into our GENTK to be able to generate the artwork at different resolution. There's multiple solutions to this.

Rather than multiplying/dividing all of the individual variables in our code by specific amount, it makes more sense to simply scale the dimensions of the canvas:

```jsx
const canvasWidth = 900;
const canvasHeight = 1200;

const scale = 2

// Multiply the canvas dimensions with the desired pixel density
canvas.width = canvasWidth * scale;
canvas.height = canvasHeight * scale;

// Scale the canvas appropriately
ctx.scale(scale, scale)
```

The rendering context provides a useful function called scale() that scales the dimensions of all the drawn graphics by the parameters that we pass into it. Before that we also need to multiply the canvas dimensions by this scale. For a scale of 2, the canvas would end up being 1800x2400 instead of 900x1200.

We also want to be able to regenerate the artwork at the new given scale with a key press, for instance if the user presses the ‘2’ key we want to double the dimensions of the canvas, if they press the ‘1’ key we want to revert back to the original dimensions.

To this end we can wrap the graphics generating code inside of a function that we can call to redraw the canvas at a different resolution when these keys are pressed:

```jsx
function redrawGraphics(scale){
  // Set the canvas dimensions multiplied by the ratio
  canvas.width = canvasWidth * scale;
  canvas.height = canvasHeight * scale;

  ctx.scale(scale, scale)

	/*
	
		Your code goes here
	
	*/
}

originalScale = 1
redrawGraphics(originalScale)
```

Here we don’t need to manually clear the canvas, it is done automatically when the width or height of the canvas is modified. Then we can simply draw the graphics as before and they will end up with the correct resolution. Notice how all of this is independent from the fxhash PRNG, and will not affect the deterministic output of the GENTK. Here’s an example of this in action:

> **CodePen demo:** <https://codepen.io/gorillasu/pen/GRzEZOO>

As for P5, its default behaviour is a little different from working with the regular HTML canvas.

It scales the P5 created canvas automatically to match the device's pixel density. The pixel density essentially just indicates how many pixels there are in a given screen, for instance retina displays (as well as many modern displays) usually have a pixel density of two. If you tried to export your artwork earlier with P5 you'll have noticed that it is exported at twice the actual dimensions that we specified in the `createCanvas()` function, so **1800x2400** instead of **900x1200**. This is done to achieve smoother graphics on higher resolution displays.

P5 provides control over this pixelDensity parameter and we can override it with the inbuilt `pixelDensity()` function. Furthermore, we can leverage this function to export outputs at different resolutions. We can simply set the canvas' and secondary graphics buffer pixel densities to a higher value to scale the graphics without a loss of resolution:

```jsx
createCanvas(canvasWidth, canvasHeight);
secondaryCanvas = createGraphics(canvasWidth, canvasHeight)

// setting the pixel density of the canvas and graphics buffer to 4
pixelDensity(4)
secondaryCanvas.pixelDensity(4)
```

We could also alternatively just set the secondary graphics buffer to a higher pixel density while keeping the display canvas at the same resolution, then simply exporting the secondary graphics buffer when the user wants to export the graphics. Then you can simply export the graphics as detailed earlier. [You might want to even go the extra mile and add in touch support for mobile devices](https://developer.mozilla.org/en-US/docs/Web/API/Touch_events/Using_Touch_Events).

### URL Parameters

Another alternative method to allow for user interaction is passing variables into the javascript code via URL parameters.

> [!NOTE]
> **URL parameters:** (also known as query parameters or query strings) are a way to include additional information in the URL of a web page. They are typically used to pass data from one page to another or to configure the behavior of a web application. URL parameters are appended to the end of a URL and are separated from the base URL by a question mark (`?`). Multiple parameters are separated by ampersands (`&`).

For example we could allow users to query a specific resolution by inputting it as a URL parameter:

```
<https://example.com/page?scale=2>
```

In the code we can check if this URL parameter exists:

```jsx
var urlParams = new URLSearchParams(window.location.search);
var scale = urlParams.get('scale');

// Check if the 'name' parameter exists
if (scale === null) {
	scale = 1
}

/*
	Rest of the code as before
*/
```

If it doesn’t we can simply fall back to a default value.
