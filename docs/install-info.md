
## Setup instructions without a prior checkout
1.  Install Python if not already installed. Test using:
    `python --version`

2.  Install [`pip`](https://pip.pypa.io/en/latest/index.html) if not already
    installed. Test using:
    `pip --version`

3.  Install git if not already installed. Test using:
    `git --version`

4.  Install the `mia` CLI tool:
    ```bash
    sudo pip install git+https://github.com/mission-impossible-android/mission-impossible-android.git
    ```
    NOTE: You can follow the setup instructions for developers if you don't want
          to install the script globally or if you don't have `sudo` access.

5.  Test if the CLI tool is working properly.
    ```bash
    mia --help
    ```

## Setup instructions using virtualenv
1.  Install Python if not already installed. Test using:
    `python --version`

2.  Install [`python-virtualenv`](https://virtualenv.pypa.io/en/latest/installation.html)
    if not already installed. Test using:
    `virtualenv --version`

3.  Clone the repository:
    ```bash
    git clone https://github.com/mission-impossible-android/mission-impossible-android.git
    ```

4.  Setup the virtual environment and install the dependencies:
    ```bash
    # Prepare the Python Virtual Environment.
    make prepare

    # Activate the newly created virtualenv.
    source bin/activate

    # Install mia once inside the Virtual Environment.
    pip install -e .
    ```

    NOTES:
    * Every time you need to use mia make sure you activate the virtualenv.
    * You can exit the virtualenv by executing `deactivate`
    * To recreate the virtual environment from scratch you can run:
      `deactivate && make clean`

5.  Test if the CLI tool is working properly:
    ```bash
    mia --help
    ```

6.  Now you can start changing files (python code or template files) and the
    changes will be visible next time you execute the `mia` command.
