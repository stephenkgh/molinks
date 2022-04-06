To set postgres password create the file "env" here containing the
password.  Use the example file as a template and modify the password:

    > cp env.example env

.git/info/exclude should contain the following to make sure the password
file is not added to git while leaving this file and env.example
untouched:

    secrets/env

