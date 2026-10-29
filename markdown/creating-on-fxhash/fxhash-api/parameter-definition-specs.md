---
title: "Parameter Definition Specs"
description: "An overview of the parameter definition specifications and the different types of parameters that are currently available."
source: https://docs.fxhash.xyz/creating-on-fxhash/fxhash-api/parameter-definition-specs
archived: https://web.archive.org/web/20260313231351/https://docs.fxhash.xyz/creating-on-fxhash/fxhash-api/parameter-definition-specs
captured: 2026-03-13
---
# Parameter Definition Specs

*An overview of the parameter definition specifications and the different types of parameters that are currently available.*

When calling `$fx.params(definition)`, a `definition` array of parameter definitions must be passed to the function. This array must be constant, which means that the same value must be passed every time the code is executed. **There cannot be any source of randomness in the definition**.

A parameter definition is an object following strict guidelines. Example:

```
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
    },
    {
        id: "color_id",
        name: "A color",
        type: "color",
    },
])
```

The **TypeScript type** for a parameter definition is:

```jsx
// a parameter definition
type ParameterDefinitionType = {
    id: string // required
    name?: string // optional, if not defined name == id
    type: "number" | "string" | "boolean" | "color" | "select" | "bigint" // required
    default?: string | number | bigint | boolean // optional
    update?: "page-reload" | "sync" | "code-driven" // optional
    options?: TYPE_SPECIFIC_OPTIONS // (optional) different options per type (see below)
}
```

### **Definition Specifications**

Each property's role is outlined as follows:

`id` required

A string identifier, which will be used to get the parameter value later in the code. This is also used to populate an object of the different parameter [id; value] when the bytes are deserialized into values when `$fx.params()` is called.

> [!CAUTION]
> **Each id must be unique! Two parameters cannot have the same id.**

---

`name` optional

A string which will be used as a display name on the minting interface. If not set, the parameter name will be its id. We recommend setting a name for every parameter so that collectors can see a nice text displayed next to the controller. We also recommend sticking with short names to keep the minting UI clean.

---

`type` required

The type of the parameter, must be one of the available types (`number`, `string`, `boolean`, `color`, `select`, `bigint`). See below for each type specification.

---

`default` optional

A default value for the parameter. If defined, when the minting interface with the controllers is loaded, the corresponding value of the controller will be set to this one. If not set, the controller value will be set to a random one within the constraints defined in the parameter options.

---

`update` optional

Specifies the update mode of the parameter. There are 3 update modes available:

- `page-reload`: (*default*) the parameter can only be updated from the fxhash UI, the whole project will be refreshed when any page-reload parameter is updated
- `sync`: the parameter can only be updated from the fxhash UI, [a `params:update` event](fxparams-api-reference.md) will be sent to the project when the parameter is update. The page is not refreshed, so you need to handle the update of the view yourself
- `code-driven`: the parameter can only be updated from your code, by[emitting a `params.update` event](fxparams-api-reference.md#usdfx.emit-eventid-data).

General overview of params update in the [fx(params) section](https://www.fxhash.xyz/doc/artist/params#fxparams-update-modes).

---

`options` optional

An object with type-specific options. Each type has specific options, described in the section below. Default values are used for each option if not defined. The default values are also described in the section below.

---

### **Parameter Types**

Each type comes with specifications:

- a list of available options
- a format in which the bytes are deserialized and made available to your code
- a kind of controller which will be displayed to modulate the parameter (this will happen outside the context of the piece itself, most often in a parent context)

#### `number`

Numbers are deserialised into [javascript float64 numbers](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number) (default javascript number type).

**Option Table**

| **Property** | **Type** | **Default** | **Description** |
| --- | --- | --- | --- |
| min | number | [Number.MIN_VALUE](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MIN_VALUE) | The minimum value the number can take. Controllers will be bound to [min; max] |
| max | number | [Number.MAX_VALUE](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_VALUE) | The maximum value the number can take. Controllers will be bound to [min; max] |
| step | number | undefined | If defined, specifies the granularity that the value must adhere to. Only values which are equal to the basis for stepping (`default` if specified, `min` otherwise, eventually the random value generated if none are specified) are valid. If undefined, any number is accepted. |

**Example:**

```
$fx.params([
{
id: "a_number",
name: "A number",
type: "number",
default: 5,
options: {
min: -10,
max: 10,
step: 1,
},
},
])
```

Corresponding controller: a slider and a text input

---

#### `string`

Strings are deserialised into a series of UTF-8 characters.

**Option Table**

| **Property** | **Type** | **Default** | **Description** |
| --- | --- | --- | --- |
| minLength | number | 0 | The minimum number of characters which has to be inputted |
| maxLength | number | 64 | The maximum number of character which can be inputted. We recommend keeping this value as low as possible, because this will always be the number of bytes sent onchain, even if a smaller string is inputted. |

**Example:**

```
$fx.params([
{
id: "a_string",
name: "A string",
type: "string",
default: "Default value",
options: {
minLength: 5,
maxLength: 32,
},
},
])
```

Corresponding controller: a text input

---

#### `boolean`

Booleans are deserialised into native javascript booleans.

*There are no available options for the boolean type.*

**Example:**

```
$fx.params([
{
id: "a_boolean",
name: "A boolean",
type: "boolean",
default: false,
},
])
```

Corresponding controller: a checkbox

---

#### `color`

Colours are serialised with 4 bytes, each byte representing the value between 0 and 255 of one channel (red, green, blue, alpha). When a colour is deserialised, it is processed into an utility-object to facilitate their usage.

The object is constructed as follows:

```jsx
{
arr: {
rgb: [25, 6, 158],
rgba: [25, 6, 158, 104],
},
hex: {
rgb: "#19069e",
rgba: "#19069e68",
},
obj: {
rgb: { r: 25, g: 6, b: 158 },
rgba: { r: 25, g: 6, b: 158, a: 104 },
}
}
```

*There are no available options for the color type.*

**Example:**

```
$fx.params([
{
id: "a_color",
name: "A color",
type: "color",
default: "abababff",
},
])
```

Corresponding controller: a color picker and a text input

---

#### `bytes`

Arbitrary data which can only be manipulated with code, not from the UI; the update mode must be **code-driven**. Allows to store bytes in an optimised way, the bytes are serialised to hexadecimal and deserialised to [Uint8Array](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Uint8Array).

| **Property** | **Type** | **Default** | **Description** |
| --- | --- | --- | --- |
| length | number | 0 | **(Required)** The maximum number of bytes which can be stored by this bytes parameter buffer. |

**Example:**

```
$fx.params([
{
id: "some_bytes",
name: "Some bytes",
type: "bytes",
update: "code-driven", // required!!
options: {
length: 4,
},
// the default value must be an Uint8Array
default: new Uint8Array([0, 255, 48, 57]),
},
])
```

---

#### `select`

A select is defined by a list of strings, where each string defines an option which can be selected. A select can take up to 256 entries. A select is stored as a single byte on-chain, which is the hexadecimal representation of a number between 0 and 255, corresponding to the index of the selected option in the array of options. When deserialised, the string of the option is extracted.

The options property of a select is required and must be an array of strings, corresponding to the available options.

**Option Table:**

| **Property** | **Required** | **Type** | **Default** | **Description** |
| --- | --- | --- | --- | --- |
| options | **Required** | string[] | / | A list of strings, corresponding to available options in the select. |

**Example:**

```
$fx.params([
{
id: "a_select",
name: "A select",
type: "select",
default: "one",
options: {
options: ["one", "two", "three", "four"],
},
},
])
```

```jsx
// output example:
// "one"
console.log($fx.getParam("a_select"))
```

Corresponding controller: a select with various options

---

#### `bigint`

A bigint is deserialized into an int64, which is the [BigInt javascript type](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt). Bigint can represent very big integer values which cannot be represented usually with javascript float numbers (between `-9223372036854775808` and `9223372036854775807`). If you need an integer value between `-9007199254740991` and `9007199254740991`, use the `number` type instead as integer values can be represented with 100% precision with float64.

**Option Table:**

| **Property** | **Type** | **Default** | **Description** |
| --- | --- | --- | --- |
| min | number | `-9223372036854775808` | The minimum value the number can take. Controllers will be bound to [min; max] |
| max | number | `9223372036854775807` | The maximum value the number can take. Controllers will be bound to [min; max] |

**Example:**

```
$fx.params([
{
id: "a_bigint",
name: "A BigInt",
type: "bigint",
default: 1458965n,
options: {
min: -1000000000000000n,
max: 1000000000000000n,
},
},
])
```

Corresponding controller: a slider and a text input
