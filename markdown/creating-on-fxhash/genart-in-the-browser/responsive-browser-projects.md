---
title: "Responsive Browser Projects"
description: "Methods for displaying your projects responsively in the browser."
source: https://docs.fxhash.xyz/creating-on-fxhash/genart-in-the-browser/responsive-browser-projects
archived: https://web.archive.org/web/20260312001935/https://docs.fxhash.xyz/creating-on-fxhash/genart-in-the-browser/responsive-browser-projects
captured: 2026-03-12
---
# Responsive Browser Projects

*Methods for displaying your projects responsively in the browser.*

It is not possible to anticipate what kind of displays or browsers your audience on fxhash may be using to view your art, they might be browsing collections on small smartphone screens or on large high resolution retina screens - it is crucial that your code always displays the generative artwork properly within any given browser window, no matter how large or small.

Moreover, your project should also be responsive and resize themselves automatically when the browser window's dimensions change.

fxhash projects primarily fall into two categories: dynamic generative artworks that span and take up the entirety of the browser window, and artworks that have fixed dimensions with a specific aspect ratio. In this page, we'll discuss some of the methods with which we can display them properly.

### Centering and Scaling a fixed aspect ratio Canvas

Projects that aim to generate outputs with a fixed aspect ratio are the more common of the two, and the more popular type of generative token. A fixed aspect ratio means that the canvas has a specific width and height. In this setting:

- The artwork should always be neatly centred within the browser window without any part of it being cut off or extending beyond the browser window.
- The artwork should maintain its aspect ratio and not be stretched along either of its axes.
- The artwork should scale with the browser window when it is resized while maintaining its aspect ratio.

CSS is an elegant and lightweight solution to centring a canvas element within the browser window. Given the following HTML body structure:

```html
<body>
  <div id="canvasContainer">
    <canvas id="myCanvas" width="900" height="1200"></canvas>
  </div>
</body>
```

We will handle the positioning of the canvas element with the following CSS rules:

```css
body {
  /* override the default margin of the html body */
  margin: 0;
}

#canvasContainer {
  height: 100vh;
  width: 100vw;

  display: flex;
  align-items: center;
  justify-content: center;
}

#myCanvas {
  max-width: 100%;
  max-height: 100vh;
}
```

The above CSS should be the content of the styles.css file in your project's directory.

Here we're mainly considering three elements: the body of the webpage that the generative artwork is displayed in, a container element that is used as a wrapper for the canvas element, and the canvas element itself.

One preliminary thing that we need to do is to remove the default margins that the `<body>` tag comes with. Having done so, we will set the canvas container to fill the entirety of the web page by setting its height and width to a `100vh` (view height) and `100vw` (view width) respectively.

We will indicate that this container div is a flexbox by setting its `display` property to `flex`. The CSS Flexbox, or Flexible Box Layout, is a popular oCSS layout model. It is designed for the arrangement of items within a container, providing a more efficient and predictable way to distribute space and align content.

This flexbox layout unlocks two further properties, namely: `align-items` and `justify-content`. These two CSS rules allow us to control the positioning of elements along the two axes of the container. By setting both of them to `center`, the canvas container taking up the entirety of the webpage, AND the canvas element being the only item inside of this flexbox, this will result in the canvas element being positioned exactly at the center of the browser window.

Now we also want the canvas element to not be cut off when the window gets smaller than the actual maximum dimensions of the canvas. This can be remedied by setting the canvas' `max-width` and `max-height` to a `100%`, indicating that we want it to stay contained within its container.

And in action this would look as follows:

> **CodePen demo:** <https://codepen.io/gorillasu/pen/WNPpYEw>

Here we also reintroduce a small margin between the canvas and the container with the following CSS rules (added to the container element):

```css
padding: 10px;
box-sizing: border-box;
```

This margin is entirely up to personal preference.

The only drawback of this CSS approach is that the canvas element will not expand beyond its maximum dimensions when the browser window grows exceedingly large, there is unfortunately no straightforward pure CSS solution to this that doesn't require a lot of additional rules. If your GENTK has large enough dimensions this shouldn't be noticeable, except on very large screens or when you modify the zoom of the browser window.

A solution to this is with some additional Javascript Code - we can scales the canvas to the size of its container with the following code:

```javascript
const canvasWidth = 400; // same as original canvas width
const canvasHeight = 400; // same as original canvas height

const resizeCanvas = function(event) {
    var containerWidth = window.innerWidth;
    var containerHeight = window.innerHeight;

    var ratio = containerWidth / canvasWidth;
    if(canvasHeight * ratio > containerHeight) {
        ratio = containerHeight / canvasHeight;
    }

    canvas.style.width = canvasWidth * ratio+"px";
    canvas.style.height = canvasHeight * ratio+"px";
}

resizeCanvas()
window.addEventListener('resize', resizeCanvas, true);
```

Here we create a function `resizeCanvas()` to handle this.

The original dimensions of the canvas are constant values and entirely up to the artist, and depend on the desired aspect ratio of the output. We need them to calculate how the canvas should be scaled to fit the browser window.

We also require the dimensions of the browser window. We can fetch these via the window object's `innerWidth` and `innerHeight` properties. These are always equal to the browser window's current effective width and height respectively, and are updated automatically when the window is resized.

The next step is a little convoluted. To explain it intuitively, we are trying to determine if the canvas should be scaled horizontally or vertically, depending on which axis allows for more space. We do so by comparing the horizontal canvas width to window width ratio with the vertical canvas height to window height ratio, subsequently using the correct one to scale the dimensions of the canvas by setting its CSS width and height through Javascript.

We run this function once at the very start when the artwork is displayed and then also pass it to a Javascript event listener that triggers whenever the browser window is resized, ensuring that the canvas is scaled when this happens.

> [!NOTE]
> **What is an event listener?**
>
> In JavaScript, an event listener is a function or piece of code that waits for a specific type of event to occur and then responds to that event by executing some predefined logic. Events can be user actions, like clicking a button, pressing a key, or resizing a window, as well as other things like data being loaded or a timer reaching a specified interval.

And in action this will work with any aspect ratio, here’s an example of a portrait aspect ratio canvas:

> **CodePen demo:** <https://codepen.io/gorillasu/pen/PoVmwWb>

Naturally, this is not the only possible solution to this end, there are numerous other methods with which you can scale the canvas.

> [!WARNING]
> When you're using a library to create the canvas element, you might have to slightly modify this CSS depending on how the library inserts the canvas element into the webpage and if it wraps the canvas inside other divs.

### Dynamic Fullscreen Projects

Generative graphics are not always simply static canvases with a fixed aspect ratio, sometimes they're interactive experiences or display animated visuals. In these scenarios it makes more sense to display things fullscreen and cover the entirety of the browser window.

Here's one solution that makes the canvas as large as the browser window without scaling or stretching the graphics:

> **CodePen demo:** <https://codepen.io/gorillasu/pen/xxMdyOG>

The graphics here don’t scale because we redraw them whenever the window is resized - in this manner we can consistently keep graphics at their respective coordinates without stretching or scaling them.

Here the canvas resizing code is even simpler:

```jsx
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
```

We simply set the width and height of the canvas to the width and height of the window object. Here we can also do without any of the CSS as we're manually setting the dimensions of the canvas. The same would be true in the case of animated graphics.

### Library specific solutions

If you're using a library like p5, it might already have some native methods out of the box to adjust the dimensions of the corresponding canvas element. In p5 a popular method to scale an artwork is by drawing the graphics to a separate graphics buffer, and then displaying this graphics buffer like an image in the webpage.

Libraries sometimes already have native, out of the box methods for the purpose of scaling the dimensions of the canvas element. P5 for instance has a method called `windowResized`() that automatically triggers whenever the browser is resized, inside of it we can call `resizeCanvas()` with the new window dimensions as parameters:

```jsx
function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}
```

This makes it very straightforward to create a fullscreen sketch:

- [p5.js Web Editor](https://editor.p5js.org/AhmadMoussa/full/3LrqdtXT1) — editor.p5js.org

In the same manner, this function is also handy for displaying artworks with a fixed aspect ratio. Especially when used in conjunction with P5's `createGraphics()` function that allows us to create a secondary canvas. Here's an example of this:

- [p5.js Web Editor](https://editor.p5js.org/AhmadMoussa/full/ZA2g5Hlzc) — editor.p5js.org

The code that achieves this is a little more involved than before, but conceptually it's very simple.

We create a secondary canvas - a graphics buffer - with a fixed size aspect ratio that will serve as the canvas onto which we draw our graphics. This secondary buffer will not be directly scaled or resized, we will actually treat like an image that will be drawn onto the original canvas. This original canvas will then be resized neatly while maintaining its aspect ratio.
