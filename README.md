# Catagolue Gun Identification Benchmark

## Setup

The script needs to be run on a linux os.


```
git clone https://github.com/conwaylife-dev/benchmark_gun_identification.git
cd benchmark_gun_identification
git submodule update --init --recursive
mkdir outputs

# Install python-lifelib inside a venv.
# Alternatively, you can install `python-lifelib` globally
# and run `python3 ./main.py old > outputs/output.txt`
python3 -m venv venv
venv/bin/pip install python-lifelib
venv/bin/python3 ./main.py old > outputs/output.old.txt
venv/bin/python3 ./main.py new > outputs/output.new.txt
```

