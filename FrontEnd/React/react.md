# React

Only required function to implement when extending React.Component class is render()

State that is maintained by a callback beyond a component should be kept by a store like Redux or commonly in top level React component.
State is propogated down to children as immutable read only properties. 

Always need to have a parent component or HTML tag wrapping return for children. 
Mixing HTML and Strings require pushing into an array in order to be interpreted correctly. 

When processing array of elements or an iterator, 
you should give unique key values to properly handle updates of the virtual dom. 
