# HTTP Parameter Pollution

Depending on back end server implementation for handling multiple parameters with the same name, falsified values may take precedence. An early example in the book shared was adding a *screen_name* parameter after a Twitter intent pop up that would cause unsuspecting people to follow a different user than what was presented by the UI.