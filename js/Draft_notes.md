**Resource links:**
---
* https://www.w3schools.com/jsref/default.asp    [Complete reference]
* https://www.w3schools.com/jsref/dom_obj_event.asp [HTML DOM events]
* https://developer.mozilla.org/en-US/docs/Web/API

**Notes:**
---
* To change **inner-html**:
```javascript
document.getElementById('idname').innerHTML = 'content'
```

* To change **HTML attribute**:
```javascript
document.getElementById('idname').attribute_name = 'attribute_value'
```

* To change HTML **style**:
```javascript
document.getElementById('idname').style.attribute_name = 'attribute_value'
```
Such as **hiding HTML elements** can be done by changing the display style:
```javascript
document.getElementById("demo").style.display = "none";
or
document.getElementById('demo').style.display = 'none';
```

* JavaScript is the default scripting language in HTML. Thus the type attribute is **not required** as
`<script type="text/javascript"> </script>`

* Any number of scripts can be placed in an HTML document.

* Scripts can be placed in the `<body>` or in the `<head>` section of an HTML page, or in both.

* Placing scripts at the bottom of the `<body>` element **improves** the display speed, because script compilation slows down the display.

* Using an **external** script:
```javascript
<script src="scriptFileName.js"></script>
```

* **Output** ways:
	* Writing into an HTML element, using `innerHTML`
	* Writing into the HTML output using `document.write()`
	* Writing into an alert box, using `window.alert()`
	* Writing into the browser console, using `console.log()`

* In HTML, JavaScript programs are **executed** by the web browser.

* Ending statements with **semicolon** is not required, but highly **recommended**.

* Single line **comments** using `//`, multiline comments using `/* */`

* Identifiers are **case sensitive**.
	* A variable declared without a value will have the value `undefined`
	* Putting a number in quotes, the rest of the numbers will be treated as **strings**, and concatenated. 
	That is, `x = "5" + 2 + 3;` will assign `"523"` to `x`
	But `x = 2 + 4 + "5" + 7;` will assign `"657"` to `x`

* **Re-declaring** a JavaScript variable will not lose its value.

* JavaScript uses the **Unicode** character set.

* The `typeof` operator returns the **type** of a variable or an expression.

* The `instanceof` operator returns `true` if an object is an instance of an object type.

* `Undefined` and `null` are equal in value but **different** in type.

* Object properties are accessed in **two** ways:
```javascript
objectName.propertyName
or
objectName["propertyName"]
```

* Data types:
	* 5 different data types that can **contain** values:
		1. string
		* number
		* boolean
		* object
		* function
		
	* 3 types of **objects**:
		1. Object
		* Date
		* Array
		
	* 2 data types that **can't** contain values:
		1. null
		* undefined
		
* `Number()` converts to a Number, `String()` converts to a String, `Boolean()` converts to a Boolean.

* The `constructor` property returns the constructor function for all JavaScript variables.

