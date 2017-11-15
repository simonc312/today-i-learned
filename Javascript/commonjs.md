CommonJS is a popular way to organize modules for libraries and server applications running NodeJS. It involves *require* statements to import modules declared by *module.exports*. 

Example:

		lodash = require("lodash");
		{foo, bar, baz} = require("../internal/path/to/module");

Taken from the Eloquent Javascript book is an example of how one might implement a toy version of the require function.

		function require(name) { 
			var code = new Function("exports", readFile(name));
			var exports = {};
			code(exports); 
			return exports;
		}

However, this version has a few shortcomings. One of which is the inability to export a file as a pure function. It expects the *exports* object to always be an object. Using a module to wrap exports allows us to override export as pure functions. 

Example:
		// sum.js
		module.exports = function sum(a, b) { return a + b;}
		// consuming_file.js
		sum = require('./sum');
		assert sum(1,1) == 2;

Revised require function with module:

		function require(name) { 
			var code = new Function("exports", "module", readFile(name));
			var exports = {}, module = {exports: exports};
			code(exports, module); 
			return module.exports;
		}

Revised require function with cache:

		function require(name) {
			if(require.cache[name]) {
				return require.cache[name]
			} 
			var code = new Function("exports", "module", readFile(name));
			var exports = {}, module = {exports: exports};
			code(exports, module);
			require.cache[name] = module.exports; 
			return module.exports;
		}

Circular dependencies

 A tricky subject in dependency management is circular dependencies, where module A depends on B, and B also depends on A. Many module systems simply forbid this. CommonJS modules allow a limited form: it works as long as the modules do not replace their default exports object with another value and start accessing each other’s interface only after they finish loading. Can you think of a way in which support for this feature could be implemented? Look back to the definition of require and consider what the function would have to do to allow this.

 The trick is to add the exports object created for a module to require’s cache before actually running the module. This means the module will not yet have had a chance to override module.exports, so we do not know whether it may want to export some other value. After loading, the cache object is overridden with module.exports, which may be a different value. But if in the course of loading the module, a second module is loaded that asks for the first module, its default exports object, which is likely still empty at this point, will be in the cache, and the second module will receive a reference to it. If it doesn’t try to do anything with the object until the first module has finished loading, things will work.

