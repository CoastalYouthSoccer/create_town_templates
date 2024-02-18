# create_town_templates

This repo creates csv files for each town from a master schedule

## Setup

This tool reads a Google sheet so the tool needs Google credentials with READ access. Additionally, the tool sends an email so credentials for sending an email are also required.

The required variables are listed in `env.sample`.

Running the tool:

1. Code is in `src` directory so `cd src`
1. Copy `env.sample` to `.env`
1. Update variable values accordingly.
1. Create a virtual environment, `python3 -m venv <virtual environment name>`
1. Active the environment, `source ./<virtual environment name>/bin/activate`
1. Install tool requirements, `pip install -r requirements`
1. Run the tool, `python schedule.py`
