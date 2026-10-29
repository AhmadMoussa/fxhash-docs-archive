---
title: "fxparams API Reference"
description: "Detailed explanations of the individual API functions related to fxparams"
source: https://docs.fxhash.xyz/creating-on-fxhash/fxhash-api/fxparams-api-reference
archived: https://web.archive.org/web/20260312012625/https://docs.fxhash.xyz/creating-on-fxhash/fxhash-api/fxparams-api-reference
captured: 2026-03-12
---
# fxparams API Reference

*Detailed explanations of the individual API functions related to fxparams*

| Function | Function Signature | Purpose Effect |
| --- | --- | --- |
| `$fx.params()` | (array) => void | Define collector-modifiable parameters for your piece by calling this with an array. |
| `$fx.getParam()` | (string) => any | Returns the value of a param via its ID. |
| `$fx.getParams()` | () => object | Returns a dictionary of all parameter key-value pairs, as currently set. |
| `$fx.getRawParam()` | (string) => string | Provides the raw parameter data (as a bytes string) as it was passed to the iteration. |
| v`on()` | (string, function, function) => function | Registers an event listener and returns a function to deregister it. |
| `$fx.emit()` | (string, any) => void | Sends an event to the parent context, useful for dynamic parameter updates from within the code. |

### `$fx.params(definition)`

The `$fx.params(definition)` function is necessary to create an fx(params) piece, it takes as input a list of parameters definitions that collectors can modulate and tweak to create their own custom iterations. Parameter definitions are object that contain a number of key/value pairs that describe the parameters.

> [!NOTE]
> You can learn more about the speficications for the these parameter definitions here:
>
> [Parameter Definition Specifications](parameter-definition-specs.md)

Here is an example of this definition array:

```
// this is how params are defined
$fx.params([
	{
		id: "number_id",
		name: "A number",
		type: "number",
		options: {
			min: -10,
			max: 10,
			step: 0.1,
		},
	},
	{
		id: "boolean_id",
		name: "A boolean",
		type: "boolean",
		//default: true,
	},
	{
		id: "color_id",
		name: "A color",
		type: "color",
	},
])
```

Invoking the `$fx.params()` function has a number of important effects:

- It informs fxhash that the project is an fx(params) project and creates the respective controllers in the UI (if the params are not `code-driven`)
- It reads the `fxparams` URL parameter, processes the bytes and converts it into values based on the provided definitions and maps them to their respective variables to generate the corresponding artwork.
- The values of the parameters are stored and made accessible throughout the artist’s code via utility functions.

> [!NOTE]
> `$fx.params()` **must be called before trying to access any parameter value with the parameter fetching functions that follow.**

### `$fx.getParam(id)`

Returns the value of a parameter based on the params definition provided to `$fx.params(definition)` and the input bytes passed to the code via URL parameters (`&fxparams={byte_sequence_here}`), the bytes sequence will be processed by `$fx.params()` when it is called.

The `$fx.getParam(id)` will fetch and return the value of parameter through its `id` as defined in your params definition:

```
// define the params
$fx.params([
	{
		id: "a_param_id", // this property will be used for $fx.getParam(id)
		name: "A random name",
		type: "boolean",
	},
	{
		id: "another_param",
		name: "Super param!",
		type: "color",
	},
])

// depending on the sequence of bytes injected into the code when it's executed,
// the values will be different

// get the value of parameter "A random name"
// output example:
// true
console.log($fx.getParam("a_param_id"))

// get the value of parameter "Super param!"
// output example:
// {
//   arr: {
//     rgb: [25, 6, 158],
//     rgba: [25, 6, 158, 104],
//   },
//   hex: {
//     rgb: "#19069e",
//     rgba: "#19069e68",
//   },
//   obj: {
//     rgb: { r: 25, g: 6, b: 158 },
//     rgba: { r: 25, g: 6, b: 158, a: 104 },
//   }
// }
console.log($fx.getParam("another_param"))
```

Depending on the type of the parameter, the fxhash snippet may apply extra processing to facilitate their usage in your code. For instance, in the case of color parameter, it will be returned in different forms. [See the parameter definition specifications](parameter-definition-specs.md) section for more details on each parameter type.

### `$fx.getParams()`

Returns an object containing all parameters, where the keys in this object are the individual parameter ids:

```
// define the params
$fx.params([
	{
		id: "a_param_id", // this property will be used for $fx.getParam(id)
		name: "A random name",
		type: "boolean",
	},
	{
		id: "another_param",
		name: "Super param!",
		type: "color",
	},
])

console.log($fx.getParams())

// output example:
// {
//   a_param_id: false,
//   another_param: {
//     arr: {
//       rgb: [25, 6, 158],
//       rgba: [25, 6, 158, 104],
//     },
//     hex: {
//       rgb: "#19069e",
//       rgba: "#19069e68",
//     },
//     obj: {
//       rgb: { r: 25, g: 6, b: 158 },
//       rgba: { r: 25, g: 6, b: 158, a: 104 },
//     }
//   }
// }

// the byte sequence injected determines the value of the parameters
```

### `$fx.getRawParam(id)`

Given a parameter id, `$fx.getRawParam(id)` returns the hexadecimal string byte sequence corresponding to that parameter, before processing and converting it into a value:

```
// define the params
$fx.params([
	{
		id: "a_param_id", // this property will be used for $fx.getParam(id)
		name: "A random name",
		type: "boolean",
	},
	{
		id: "another_param",
		name: "Super param!",
		type: "color",
	},
])

// depending on the sequence of bytes injected into the code when it's executed,
// the values will be different

// get the value of parameter "A random name"
// output example:
// "01"
console.log($fx.getRawParam("a_param_id"))

// get the value of parameter "Super param!"
// output example:
// "19069e68"
console.log($fx.getParam("another_param"))
```

### `$fx.emit(eventId, data)`

This function is mainly used for the purpose of updating parameters that have their `update` mode set to `code-driven`. As its name suggests, `$fx.emit(eventId, data)` allows you to emit events (think of it like a signal), to an fxhash specific pipeline of events, which can then be listened to by the `$fx.on()` function. Currently there is only one type of event that is supported, namely the `param:update` signal.

Additionally, this event can also carry a payload which can be specified with the second input parameter of the `$fx.emit` function, the `data` variable. The `data` variable should be an object where the key/value pairs are the parameter ids and the updated associated values respectively. This is still subject to the constraints of the parameter (as set by its parameter definition), so for instance if a number between 0 and 10 is expected and you pass a value of 12, it will clamp to 10. You are not required to pass all the parameters in the data, only those which need to be updated.

Here’s an example, let’s first set up a couple of parameters:

```
// define your parameters
$fx.params([
	{
		id: "mouse_x",
		type: "number",
		// a code-driven parameter
		update: "code-driven",
	},
	{
		id: "number_2",
		type: "number",
		// a code-driven parameter
		update: "code-driven",
	},
	{
		id: "number_3",
		type: "number",
		// a normal parameter, cannot update with params:update
		update: "page-reload",
	},
])
```

And then send out an event whenever we move the mouse:

```jsx
// example: when the mouse moves, we update the first parameter
window.addEventListener("mousemove", evt => {
	const X = evt.clientX / window.innerWidth // normalized X position of mouse
	// we request the update of a parameter
	$fx.emit("params:update", {
		mouse_x: X,
	})
})
```

Here we used a native Javascript eventlistener to detect whenever the mouse is moved, making it in turn trigger the `$fx.emit()` function to update the `mouse_x` parameter.

Following is the typescript definition of the `$fx.emit` function:

```jsx
type FxEmitFunction = (
	eventId: string
	data: any
) => void
```

### `$fx.on(eventId, handler, onDone)`

The `$fx.on()` function listens to events in the fxhash pipeline that are emitted by `$fx.emit()`. Currently there is only one type of event that is supported, namely the `param:update` event. `$fx.on()` can then trigger functions when this event is registered and certain conditions are met. Note that the `eventId` must match an existing `eventId` that you can subscribe to.

The `handler` is the function that is called when the event is triggered. Additionally you can opt-out of the default behaviour of an event handler by returning `false` from the handler. The `onDone` function is called as the last thing of any event, e.g. after the default behaviour of the event was applied.

```
// define your parameters
$fx.params([
	{
		id: "number_id",
		type: "number",
		update: "sync",
	},
])

function main() {
	// render artwork
}

$fx.on(
	"params:update", // subscribe to the params update event
	newValues => {
		// opt-out param update when number_id is 5
		if (newValues.number_id === 5) return false
		// opt-in any other param value update
		return true
	},
	() => main() // render artwork when event was handled
)
```

Following is the typescript definition of the `$fx.on` function:

```jsx
type FxOnFunction = (
	eventId: string
	handler: (...args) => boolean | Promise<boolean>
	onDone: (optInDefault: boolean, ...args) => void
) => () => void
```

The function returned by the `$fx.on` function can be called to remove the registered event listener.

```jsx
const removeListener = $fx.on("params:update", newValues => {
	// do something
})

removeListener() // <-- Will remove the event listener
```

Note: there are 2 ways to apply changes to the UI when you emit a parameter from the code:

```
// FIRST WAY
// Emit the update, and update the view only when receiving the params:update
// back. This ensures a proper flow of data, and a proper sync of the minting
// UI and your project
window.addEventListener("mousemove", evt => {
	const X = evt.clientX / window.innerWidth
	$fx.emit("params:update", {
		mouse_x: X,
	})
})

$fx.on("params:update",

() => {}, // do nothing to check the params received

() => { // once the update is fully registered, update the view
		draw()
		// in this case draw() can rely on $fx.getParam("mouse_x") to be synced with
		// the up-to-date value
	}
)
```

```jsx
// SECOND WAY
// Custom draw logic where the params effects are applied right after emitting
// the update
window.addEventListener("mousemove", evt => {
	const X = evt.clientX / window.innerWidth
	$fx.emit("params:update", {
		mouse_x: X,
	})

	// here trigger a draw, but you need to handle the change in value manually,
	// as $fx.getParam("mouse_x) will point to the old value
	draw(X)
})
```
