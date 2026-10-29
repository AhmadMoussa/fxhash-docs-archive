---
title: "Canvas element & API"
description: "An explanation of the HTML canvas element and the Canvas API"
source: https://docs.fxhash.xyz/creating-on-fxhash/genart-in-the-browser/canvas-element-and-api
archived: https://web.archive.org/web/20260312044332/https://docs.fxhash.xyz/creating-on-fxhash/genart-in-the-browser/canvas-element-and-api
captured: 2026-03-12
---
# Canvas element & API

*An explanation of the HTML canvas element and the Canvas API*

The canvas element was first introduced by Apple in 2004 and was later standardised across various web browsers with HTML5. Today, the HTML5 canvas element is widely considered the go-to choice for rendering graphics in modern web browsers. One key reason for this is its built-in Canvas API: a set of functions designed for the purpose of drawing to this digital drawing surface.

> [!NOTE]
> **What is the** **HTML** `<canvas>` **element?**
>
> The `<canvas>` element is a special HTML element that makes it possibly to dynamically draw graphics, animations, and interactive content on a web page using JavaScript. In essence it is a a rectangular bitmap, a grid of pixels, that allows the creation and manipulation of graphics within a web browser.
>
> It’s not only a powerful tool for the creation of generative art but also web-based games, data visualisations, charts, drawings, and other interactive multimedia content in the browser.

The canvas element comes with its own associated canvas API, which provides convenience functions that make the creation of graphics on this bitmap much easier, rather than requiring the artist to manually update individual pixels to create certain shapes, it handles this for us. The most comprehensive resource for this canvas element can be found over on the MDN web docs:

- [Canvas API - Web APIs | MDN](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API) — MDN Web Docs

What's more is that over the years numerous libraries have been developed on top of this canvas API to further simplify writing graphics generating code. For the purpose of making generative art, some of these libraries have become increasingly popular in recent years; they are frequently used to build fxhash projects and we will have a look at some of them throughout the next sections.

In this section, we'll mainly talk about how to create a canvas element in a web page and how to use the functions that the canvas API provides to draw to it.

### **The Canvas Element**

A canvas element can simply be created by using the `<canvas>` tag in our HTML document:

```jsx
<canvas width="400" height="400"></canvas>
```

The canvas element comes at a default width of 300 pixels and default height of 150 pixels. We can however specify our own dimensions through the `width` and `height` HTML attributes - here we set them to 400 pixels each, resulting in a square aspect ratio canvas.

A minimal webpage with a canvas element would look as follows:

```jsx
<!DOCTYPE html>
<html>
	<head>
		<title>Canvas Example</title>
	</head>
	<body>
		<canvas id="myCanvas" width="400" height="300"></canvas>
	</body>
</html>
```

And here's what this would look like:

> **CodePen demo:** <https://codepen.io/gorillasu/pen/rNPjWrm>

The canvas element is transparent by default. Here we're colouring it in a dark grey with some inline CSS to differentiate it from the background and make it visible:

```css
style="background-color: darkgray;"
```

This doesn’t look like much yet, but it is the foundation for drawing graphics into the browser.

### **The different Rendering Contexts**

Drawing to the canvas element doesn't happen directly via the canvas API per se, but rather via a rendering context that this canvas API exposes. Rendering contexts are essentially different drawing modes in which we can manipulate graphics on an HTML5 `<canvas>` element.

Each type of rendering context provides specific capabilities and methods for working with graphics in different ways. Selecting which one is more suitable for your purposes entirely depends on the generative artwork you’d like to create.

> [!NOTE]
> **What is a rendering context?**
>
> A rendering context in the context of the HTML `canvas` element refers to the object that provides methods and properties for drawing on the canvas. The rendering context is an interface to a drawing surface and is obtained from the canvas element.

The Canvas API mainly provides two rendering contexts, the 2D context and the WebGL context:

- **The 2D Rendering Context (2D Context):** is the more commonly used rendering context. It provides methods and properties for creating and manipulating 2D graphics on the canvas. It allows us to draw shapes, text, images, apply styles, create animations, and more. [Reference for the 2D rendering context.](https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D)
- **The WebGL Rendering Context:** short for Web Graphics Library, is a JavaScript API that is more commonly used for rendering 3D graphics within a `<canvas>` element using the power of hardware acceleration. Based on OpenGL, it provides a more advanced and complex way to create interactive 3D graphics and high-performance visualizations on the web. This rendering context comes in two flavors WebGL and WebGL2, where the latter is an updated version of the former that provides more features. [Reference for the WebGL rendering context.](https://developer.mozilla.org/en-US/docs/Web/API/WebGLRenderingContext)

In other words, if you want to display 2D graphics go for the 2D context, and for 3D stuff the WebGL rendering context is more suitable.

### **Drawing to the Canvas**

Having created the canvas element we can now make use of one of these rendering contexts to draw some graphics to it. To this end, we first need to fetch the canvas element from the DOM of our webpage. This can be done as follows:

```javascript
// We conveniently gave the canvas element an id to fetch it from the DOM.
const canvas = document.getElementById('myCanvas');
```

When we created the canvas element, we conveniently gave it an id attribute allowing us to now fetch a reference to it from the DOM with the [`document.getElementById()`](https://developer.mozilla.org/en-US/docs/Web/API/Document/getElementById) function.

> [!NOTE]
> **What is the DOM?**
>
> The DOM, or Document Object Model, is a programming interface for web documents. It represents the structure of a document as a tree of objects, where each object corresponds to a part of the document, such as elements, attributes, text, etc. The DOM provides a way for programs (typically scripts written in languages like JavaScript) to manipulate the structure, style, and content of web documents dynamically.

Now we can select which rendering context we’d like to use:

```javascript
// The rendering context can be accessed via the getContext() function.
const ctx = canvas.getContext('2d');
```

For now we'll make use of the 2d rendering context, otherwise we could also specify `‘webgl’` here. We can now use this rendering context's functions to draw to the canvas:

```javascript
// This draws a blue rectangle to the canvas
ctx.fillStyle = 'blue';
ctx.fillRect(50, 50, 200, 100);
```

And here's what this would look like:

> **CodePen demo:** <https://codepen.io/gorillasu/pen/jOdyyRZ>

All of this can be done within a `<script>` tag inside the same HTML document directly underneath our `<canvas>` tag:

```html
<!DOCTYPE html>
<html>
	<head>
		<title>Canvas Example</title>
	</head>
	<body>
		<canvas id="myCanvas" width="400" height="400" style="background-color: darkgray;"></canvas>
		<script>
				// We conveniently gave the canvas element an id to fetch it from the DOM.
				const canvas = document.getElementById('myCanvas');

				// The rendering context can be accessed via the getContext() function.
				const ctx = canvas.getContext('2d');

				// This draws a blue rectangle to the canvas
				ctx.fillStyle = 'blue';
				ctx.fillRect(50, 50, 200, 100);
		</script>
	</body>
</html>
```

But alternatively we could also place this graphics drawing code in it’s own individual JS file and reference it.

### Animated Graphics

Static graphics are only the tip of the ice-berg however, we can also display animated graphics on this canvas element. This can be achieved via the [`requestAnimationFrame()`](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame) function—here’s an example:

> **CodePen demo:** <https://codepen.io/gorillasu/pen/vYbZxVN>

And the code that powers this animation, looks as follows:

```javascript
// Fetching the Canvas and Context
const canvas = document.getElementById('myCanvas');			
const ctx = canvas.getContext('2d');

let counter = 0

// A function which will power the animation
function draw(){

	// Filling the entire canvas with colored rectangle
	ctx.fillStyle = "white";
	ctx.fillRect(0, 0, canvas.width, canvas.height);
	
	// Setting the color for the rectangles
	ctx.fillStyle = "black";

	// A little trigonometry to make the rectangles rotate in a circle
	
	for(let a = counter; a < Math.PI*2+counter; a+=Math.PI*2/20){
		let x = 200 + 100 * Math.cos(a)
		let y = 200 + 100 * Math.sin(a)
		
		ctx.fillRect(x, y, 10, 10)
	}
	
	counter+=.01
	requestAnimationFrame(draw)
}

draw()
```

We created a function called `draw()` that creates a spinning circle of rectangles. Within it we draw a white rectangle that spans the entire canvas (as a background), as well as a loop that uses trigonometry to draw a number of black rectangles around the circumference of a circle. The white rectangle is used to reset the canvas and cover the previous graphics that have already been drawn in previous invocations of the `draw()` function.

Towards the end of it we invoke the `requestAnimationFrame()` function and pass in the `draw()` function itself as an argument. By doing so, the `requestAnimationFrame()` function will execute the draw function again once it has completed, this causes the `draw()` function to run continuously and make the spinning circle move forward by means of a variable called `counter`, that is incremented each time the `draw()` function is executed. A note here, is that this function doesn’t necessarily need to be named `draw()`, it can have a different signature as well. You can find more explanations and examples of animations [here](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Basic_animations).

This concludes this short primer on the HTML canvas element. In the next sections we will discuss some of the important aspects that come into play when we try to build a generative token with this canvas element, such as positioning it neatly in the browser window, handling user input as well as using some of the libraries that are built around the canvas element.
