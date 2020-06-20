**Resource Links:**

- http://www.formencode.org/en/latest/Validator.html

**Notes:**

- The basic metaphor for validation is `to_python` and `from_python`.

- `formencode.Invalid` exceptions generally give a **good, user-readable **error message about the problem with the input. 

-  The best way **to read** about the individual validators available in the `formencode.validators` module is to read about `validators` and `national`.

- The class `formencode.FancyValidator` is the **superclass** for most validators in FormEncode.

- `formencode.FancyValidator`adds a number of extra **features**, and then calls the **internal** `_convert_to_python()` method, which is the method one will typically write.
Its only concern is the *conversion* part, not the *validation* part.

- Further validation can be done in **internal** methods `_validate_python()` or `_validate_other()`.

- `_validate_python()` **doesn’t** have any return value, it simply raises an exception if it needs to.

- The external method `to_python()` cares about the **extra features** such as the `if_empty` parameter, and uses the internal methods to do the actual conversion and validation;
**first** it calls `_validate_other()`,
**then** `_convert_to_python()`
and **at last** `_validate_python()`.

- To validate **different** attributes with different validators, use subclass of `formencode.Schema`.

- To do simple validation of a complete form is with `formencode.schema.SimpleFormValidator`. This class wraps a simple **function** that you write.

- To validate **list** of items, use `formencode.foreach.ForEach()`.

- Any arguments you pass to the **constructor** will be used to set instance variables.

- The use of `self.message(...)` is meant to make the messages easy to **format** for different environments, and **replacable** (with translations, or simply with different text).

- Validators use instance variables to **store** their customization information. You can use either *subclassing* or *normal instantiation* to set these.

- There are **several options** that most validators support (including your own validators, if you subclass from `formencode.FancyValidator`):
	- `if_empty`
	- `not_empty`
	- `strip`
	- `if_invalid`
	- `if_invalid_python`
	- `accept_python`
	- `if_missing`
	
- Whatever else you **need to pass** in any data, just put it in the `state` object as an attribute, then look for that attribute in your validator.

- **During** a `Schema` (dictionary) validation the instance variable `key` and `full_dict` will be added – `key` is the current key (i.e., validator name), and `full_dict` is the rest of the values being validated.
**During** a `ForEach` (list) validation, `index` and `full_list` will be set.

- Besides the string error message, `formencode.Invalid` exceptions have a few other instance variables:
	- `value`
	- `state`
	- `msg`
	- `error_list`
	- `error_dict`
	- `unpack_errors()`
	
- You can **overwrite error messages** by using your own`messages = {"key": "text"}` in the class statement, or as an argument when you call a class. Either way, you do not lose messages that you do not define, you only overwrite ones that you specify.