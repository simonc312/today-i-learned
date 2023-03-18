# Javascript 

## Numbers

You can use scientific notation by adding an e to represent exponent. 
		
		42e10 == 42 * Math.pow(10, 10)

NaN represents a special number type usually caused by calculation errors like dividing by 0. 
		
		NaN == NaN == false

Nonsensical output will never match.

Infinity and -Infinity represent the max and min numbers possible useful as default comparison values. 

## Big Int
The BigInt data type allows for accurately storing and operating on large (whole) numbers, which prevents errors produced by JavaScript storing numbers as floats. They can either be constructed using the BigInt() constructor (preferably with strings to prevent inaccuracies) or by appending n at the end of a number.


## Strings

`String.replace(substringMatch, substringReplace)` function only replaces first occurance before returning.  
		
		"strings".replace("s", "S") == "Strings"

replace(regexMatchGroup, substringReplace) function replaces all occurances. 

		"strings".replace(/s/g,"S") == "StringS"

The `/g` stands for a global search regex flag. 

ES2021
`String.replaceAll()` Replace all instances of a substring in a string, instead of always using a regular expression with the global flag (/g)

## Booleans

		(null == undefined) != false

		false == 0 == NaN == "" 

Without type coercion: 

		false !== 0 !== NaN !== ""

## Symbols

ES6 added Symbol as a new primitive type. Unlike other primitive types such as number, boolean, null, undefined, and string, the symbol type doesn’t have a literal form.

To create a new symbol, you use the global Symbol() function as shown in this example:

	let b = Symbol('beer');

The Symbol() function creates a new unique value each time you call it:

	console.log(Symbol() === Symbol()); // false

The Symbol() function accepts a description as an optional argument. The description argument will make your symbol more descriptive.

The following example creates two symbols:

	pendingStatus = Symbol('pending'),
    completeStatus = Symbol('complete');

You can access the symbol’s description property using the toString() method.

ES6 provides you with a global symbol registry that allows you to share symbols globally. If you want to create a symbol that will be shared, you use the `Symbol.for()` method instead of calling the `Symbol()` function.

The `Object.getOwnPropertySymbols()` method returns an array of own property symbols from an object.

ES6 provides predefined symbols which are called well-known symbols. The well-known symbols represent the common behaviors in JavaScript. Each well-known symbol is a static property of the Symbol object.

- The Symbol.hasInstance is a symbol that changes the behavior of the instanceof operator
- The Symbol.iterator specifies whether a function will return an iterator for an object.
- The Symbol.isConcatSpreadable property is a Boolean value that determines whether an object is added individually to the result of the concat() function.
- The Symbol.toPrimitive method determines what should happen when an object is converted into a primitive value.

## Assignment

`||=` assign value only if previous value was 'falsy'

`&&=` assign value only if previous value was 'truthy'

`??=` assign value only if previous value was 'undefined' or 'null'


## Reserved Keywords

	break case catch class const continue debugger
	default delete do else enum export extends false
	finally for function if implements import in
	instanceof interface let new null package private
	protected public return static super switch this
	throw true try typeof var void while with yield async await

## Browser commands

Besides console.log and alert there are also:

-  returns input entered by user
		
		prompt("What do you want to ask","user input hint")

-  returns true or false based on user input 

		confirm("Confirmation message")

## Functions

The **bind()** function which acts as a wrapper for passing objects, this context, or partially evaluating functions.
		
		class Foo {
			foo(a, b, c) {
				return a - b + c;
			}

			fooBound(a, b) {
				return this.foo.bind(this, a, b);
			}
		}
		new Foo().fooBound(1, 2)(3) == 2;

The **apply()** function also takes a this context as its first parameter, and immediately calls the function with the rest of parameters passed in array.
The **call()** function is the same as apply except it doesn't need to use an array to contain the function parameters.

		function foo(a, b, c) {
			return a - b + c;
		}
		foo.apply(null, [1, 2, 3]) == 2;
		foo.call(null, 1, 2, 3) == 2;

## WTFs

undefined and null operators are very similar. 

typeof null is object 

You can attempt to access a property with bracket notation. 

		foo["bar"] == foo.bar if property exits else undefined

There is no deep comparison operation for objects only shallow comparison.
So even if objects possess identical content, == will return false. 

Able to accept variable number of parameters for a function by referencing **arguments** as array.

		var journal = [];
		function addEntry ( ) {
			var entry = { events : [] };
			for ( var i = 0; i < arguments.length ; i++)
				entry.events.push(arguments [ i ]);
			journal.push(entry);
		}
		addEntry ("wake up", "brush teeth", "breakfast burrito", "chase down shuttle" , "read novella", "burn midnight oil");


## Dynamic Imports

Relatively new feature more broadly compatible on major browsers by start of 2020. The import() call is a syntax that closely resembles a function call, but import itself is a keyword, not a function. You cannot alias it like const myImport = import, which will throw a SyntaxError. Returns a promise which fulfills to a module namespace object: an object containing all exports from moduleName.

- Importing modules based on user interaction
- Importing modules for their side effects
- Importing modules based on browser vs server side environment
- 
- Importing modules with a non-literal specifier.

Dynamic imports allow any expression as the module specifier, not necessarily string literals.
Here, we load 10 modules, /modules/module-0.js, /modules/module-1.js, etc., in parallel, and call the load functions that each one exports.

		Promise.all(
		Array.from({ length: 10 }).map((_, index) =>
			import(`/modules/module-${index}.js`),
		),
		).then((modules) => modules.forEach((module) => module.load()));

## Adding Error Cause

An optional cause can now be specified for Errors, which allows specifying of the original error when re-throwing it.

	try {
	try {
		deliverProduct();
	} catch (err) {
		throw new Error('Delivering product failed.', { cause: err });
	}
	} catch (err) {
	console.log(err.cause); // IllegalStateError: product is not ready
	}