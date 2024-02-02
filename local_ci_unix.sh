#! /usr/bin/bash

# DEFAULTS
TOP_MPY_DIR=$PWD
UNIX_VARIANT="standard" 
UNIX_VARIANT_DIR=$TOP_MPY_DIR/ports/unix/variants 


OK="[\u001b[32;1m OK \u001b[0m]"
FAIL="[\u001b[31;1m FAILED \u001b[0m]"
SKIP="[\u001b[33;1m SKIP\u001b[0m ]"


echo -e "PORT: unix CI [\u001b[32;1m RUNNING \u001b[0m]"
source tools/ci.sh

# CUSTOM CONFIG
source .env


# ports/unix
function ci_unix_build_helper_remote {
    # make ${MAKEOPTS} -C mpy-cross
    SUBMODULES="lib/mbedtls lib/micropython-lib lib/berkeley-db-1.xx" 
    git submodule sync $SUBMODULES
    git submodule update --init $SUBMODULES
    make ${MAKEOPTS} -C ports/unix "$@" deplibs

    make ${MAKEOPTS} -C ports/unix "$@" clean 
    make ${MAKEOPTS} -C ports/unix "$@" -j8
    return $?
}

function ci_unix_standard_build_remote {
    ci_unix_build_helper_remote VARIANT_DIR=$UNIX_VARIANT_DIR/$UNIX_VARIANT

    if [ $? -eq 0 ];
    then
      ci_unix_build_ffi_lib_helper gcc
    else
      exit 1
    fi
    
}

function ci_unix_run_tests {
    variant=$1
    shift
    micropython=../ports/unix/build-$variant/micropython
    make -C ports/unix VARIANT_DIR=$UNIX_VARIANT_DIR/$variant "$@" test_full
    return $?
}


function ci_unix_run_multi_tests {
    variant=$1
    shift
    micropython=../ports/unix/build-$variant/micropython
    (cd tests && MICROPY_CPYTHON3=python3 MICROPY_MICROPYTHON=$micropython ./run-multitests.py multi_net/*.py)
    return $?
}


function ci_unix_run_perfbench {
    variant=$1
    shift
    micropython=../ports/unix/build-$variant/micropython
    (cd tests && MICROPY_CPYTHON3=python3 MICROPY_MICROPYTHON=$micropython ./run-perfbench.py 1000 1000)
    return $?
}


# BUILD

ci_unix_standard_build_remote
if [ $? -eq 0 ];
then
  echo -e "PORT: unix BUILD: $OK"
else
  echo -e "PORT: unix BUILD: $FAIL" >&2
  exit 1
fi

# TESTS
echo "Running tests..."
ci_unix_run_tests $UNIX_VARIANT
test_result=$?

if [ $test_result -eq 0 ];
then
  echo -e "PORT: unix TESTS: $OK"
else
  echo -e "PORT: unix TESTS: $FAIL" >&2
  # exit 1
fi


echo "Running multinet tests..."
ci_unix_run_multi_tests $UNIX_VARIANT
multi_test_result=$?

if [ $multi_test_result -eq 0 ];
then
  echo -e "PORT: unix MULTINET TESTS: $OK"
else
  echo -e "PORT: unix MULTINET TESTS: $FAIL" >&2
  # exit 1
fi

# TODO: add ENV VARIABLE TO RUN CUSTOM TESTS

# BENCH

echo "Running perfbench..."
ci_unix_run_perfbench $UNIX_VARIANT
perfbench_result=$?
if [ $perfbench_result -eq 0 ];
then
  echo -e "PORT: unix PERFBENCH: $OK"
else
  echo -e "PORT: unix PERFBENCH: $FAIL" >&2
  # exit 1
fi

# CI RESULT
if [ $test_result -eq 0 ];
then
    :
else 
    exit 1 
fi 


if [ $multi_test_result -eq 0 ];
then
    :
else 
    exit 1 
fi 


if [ $perfbench_result -eq 0 ];
then
    :
else 
    exit 1 
fi 

