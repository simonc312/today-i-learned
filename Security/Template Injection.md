# Template Injection

A template engine is code used to create dynamic websites, emails, etc. When the template is rendered, the engine replaces placeholders with their content so that
app logic is separated from view logic.

Templating engines also provide features such as user input sanitization, HTML generation, and easy maintenance. However these features don’t make templating engines bug free.

## Server Side 

After determining the template engine used by servers, testing payloads to evaluate expressions can identify what does not get sanitized safely.

## Client Side

Can occur with client side template engines like AngularJS `{{}}` and React `{}` to achieve XSS but not remote code execution.
Good thing that by default, React DOM escapes any values embedded in JSX before rendering them. So you can never inject anything that’s not explicitly written in your application. Everything is converted to a string before being rendered.

## Examples

In 2016 the Uber rider profile name would evaluate as an unsanitized expression when sending emails to allow for arbitrary code execution. 

Outdated Ruby on Rails versions had vulnerabilities that would allow for server side remote code execution through its default ERB template engine.