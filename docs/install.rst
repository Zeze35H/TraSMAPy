Installing TraSMAPy
===================

You can install TraSMAPy using the following command:

    pip install "git+https://github.com/JoaoCostaIFG/TraSMAPy.git"

This will install TraSMAPy and all its dependencies.

Virtual environment
-------------------

Optionally, you can create a virtual environment and install TraSMAPy inside it:

    python3 -m venv venv
    source venv/bin/activate
    pip install "git+https://github.com/JoaoCostaIFG/TraSMAPy.git"

Don't forget to activate the virtual environment before using TraSMAPy, and to add the `venv` directory to your `.gitignore` file.

Development mode
----------------

If you want to contribute to TraSMAPy, you can clone the repository, and install it in development mode:

    git clone "https://github.com/JoaoCostaIFG/TraSMAPy.git"
    cd TraSMAPy
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e .
