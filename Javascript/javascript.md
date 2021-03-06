# Javascript 

## Numbers

You can use scientific notation by adding an e to represent exponent. 
		
		42e10 == 42 * Math.pow(10, 10)

NaN represents a special number type usually caused by calculation errors like dividing by 0. 
		
		NaN == NaN == false

Nonsensical output will never match.

Infinity and -Infinity represent the max and min numbers possible useful as default comparison values. 


## Strings

replace(substringMatch, substringReplace) function only replaces first occurance before returning.  
		
		"strings".replace("s", "S") == "Strings"

replace(regexMatchGroup, substringReplace) function replaces all occurances. 

		"strings".replace(/s/g,"S") == "StringS"

The /g stands for a global search regex flag. 

## Booleans

		(null == undefined) != false

		false == 0 == NaN == "" 

Without type coercion: 

		false !== 0 !== NaN !== ""

## Reserved Keywords

break case catch class const continue debugger
default delete do else enum export extends false
finally for function if implements import in
instanceof interface let new null package private
protected public return static super switch this
throw true try typeof var void while with yield

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
