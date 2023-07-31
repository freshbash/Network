# Network

A text-based twitter clone

## Features
- Create Posts
- Follow/Unfollow users
- Like/Unlike posts
- Edit posts
- Edit profile
- Pagination of posts

### Learnings while developing

1. In order to incorporate React into our project, we need a bundler. A bundler is a program that bundles all React components into one file and converts the code into browser-understandable code. The browser does not understand JSX(which can be mitigated, albeit iefficiently) and more importantly it does not understand
code split across multiple files. So, either we use a bundler or we put all our React code into one file.
For better readability, we should use a bundler.

2. While making the project production-ready, we need to set SECURE_SSL_REDIRECT=True in settings.py.
This redirects all http requests to an equivalent https url. This may cause some of the CI tests to fail.
So we need to create a separate settings file with SECURE_SSL_REDIRECT set to False and intructing
django to use that file for testing purposes.
